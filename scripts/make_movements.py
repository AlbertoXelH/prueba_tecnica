from django.db import transaction
from apps.customers.models import Customer
from apps.locations.models import Warehouse
from apps.catalog.models import Product
from apps.inventory.models import MovementType, Stock
from apps.inventory.services import MovementInput, record_movement

@transaction.atomic
def run():
    total_in = 0
    total_out = 0
    total_movs = 0

    for c in Customer.objects.order_by("name"):
        wh = Warehouse.objects.filter(branch__customer=c).order_by("code").first()
        if not wh:
            print(f"SKIP {c.name}: no tiene almacenes")
            continue

        productos = Product.objects.filter(customer=c).order_by("sku")
        if not productos.exists():
            print(f"SKIP {c.name}: no tiene productos")
            continue

        for i, p in enumerate(productos, start=1):
            qty_in = 10 + (i * 2)          # IN siempre > OUT
            qty_out = max(1, qty_in // 3)  # OUT menor que IN

            m_in = record_movement(MovementInput(MovementType.IN, wh.id, p.id, qty_in))
            m_out = record_movement(MovementInput(MovementType.OUT, wh.id, p.id, qty_out))

            s = Stock.objects.get(warehouse=wh, product=p)

            total_in += qty_in
            total_out += qty_out
            total_movs += 2

            print(f"{c.name} | {p.sku} | WH={wh.code} | IN {qty_in} -> PDF: http://127.0.0.1:8000/api/movements/{m_in.id}/pdf/")
            print(f"{c.name} | {p.sku} | WH={wh.code} | OUT {qty_out} -> PDF: http://127.0.0.1:8000/api/movements/{m_out.id}/pdf/")
            print(f"   Stock final en ese almacén: {s.quantity}")
            print("-" * 80)

    print(f"OK. Movimientos creados: {total_movs} | Total IN={total_in} | Total OUT={total_out}")

run()
