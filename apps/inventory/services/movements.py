from dataclasses import dataclass
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from apps.inventory.models import Movement, MovementType, Stock
from .errors import InsufficientStock
from .pdfs import build_movement_pdf

@dataclass(frozen=True)
class MovementInput:
    movement_type: str
    warehouse_id: int
    product_id: int
    quantity: int

@transaction.atomic
def record_movement(data: MovementInput) -> Movement:
    stock, _ = Stock.objects.select_for_update().get_or_create(
        warehouse_id=data.warehouse_id,
        product_id=data.product_id,
        defaults={"quantity": 0},
    )

    before = stock.quantity

    if data.movement_type == MovementType.IN:
        after = before + data.quantity
    elif data.movement_type == MovementType.OUT:
        if data.quantity > before:
            raise InsufficientStock(available=before, requested=data.quantity)
        after = before - data.quantity
    else:
        raise ValueError("Invalid movement_type")

    stock.quantity = after
    stock.save(update_fields=["quantity", "updated_at"])

    movement = Movement.objects.create(
        movement_type=data.movement_type,
        warehouse_id=data.warehouse_id,
        product_id=data.product_id,
        quantity=data.quantity,
        stock_before=before,
        stock_after=after,
    )

    movement = Movement.objects.select_related("warehouse__branch__customer", "product").get(pk=movement.pk)

    pdf_bytes = build_movement_pdf(
        {
            "movement_type": movement.get_movement_type_display(),
            "date": timezone.localtime(movement.occurred_at).strftime("%Y-%m-%d %H:%M:%S"),
            "product": str(movement.product),
            "quantity": movement.quantity,
            "warehouse": str(movement.warehouse),
            "stock_before": movement.stock_before,
            "stock_after": movement.stock_after,
        }
    )

    movement.pdf.save(f"{movement.id}.pdf", ContentFile(pdf_bytes), save=True)
    return movement
