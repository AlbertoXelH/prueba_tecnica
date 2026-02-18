from dataclasses import dataclass
from django.db import transaction
from apps.inventory.models import Movement, MovementType, Stock
from .errors import InsufficientStock

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

    return Movement.objects.create(
        movement_type=data.movement_type,
        warehouse_id=data.warehouse_id,
        product_id=data.product_id,
        quantity=data.quantity,
        stock_before=before,
        stock_after=after,
    )
