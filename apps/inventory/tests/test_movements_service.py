import pytest
from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from apps.catalog.models import Product
from apps.inventory.models import MovementType, Stock
from apps.inventory.services import MovementInput, InsufficientStock, record_movement

pytestmark = pytest.mark.django_db


def setup_ctx():
    c = Customer.objects.create(name="ACME")
    b = Branch.objects.create(customer=c, name="Centro")
    w = Warehouse.objects.create(branch=b, name="Principal")
    p = Product.objects.create(customer=c, sku="SKU-1", name="Producto 1")
    return w, p


def test_in_and_out_updates_stock_and_records_before_after():
    w, p = setup_ctx()

    m1 = record_movement(MovementInput(MovementType.IN, w.id, p.id, 10))
    assert m1.stock_before == 0
    assert m1.stock_after == 10

    m2 = record_movement(MovementInput(MovementType.OUT, w.id, p.id, 4))
    assert m2.stock_before == 10
    assert m2.stock_after == 6

    s = Stock.objects.get(warehouse=w, product=p)
    assert s.quantity == 6


def test_out_cannot_exceed_stock():
    w, p = setup_ctx()
    record_movement(MovementInput(MovementType.IN, w.id, p.id, 3))

    with pytest.raises(InsufficientStock) as e:
        record_movement(MovementInput(MovementType.OUT, w.id, p.id, 5))

    assert e.value.available == 3
    assert e.value.requested == 5
