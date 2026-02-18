import pytest
from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from apps.catalog.models import Product
from apps.inventory.models import MovementType
from apps.inventory.services import MovementInput, record_movement

pytestmark = pytest.mark.django_db


def test_movement_generates_pdf_file():
    c = Customer.objects.create(name="ACME")
    b = Branch.objects.create(customer=c, name="Centro")
    w = Warehouse.objects.create(branch=b, name="Principal")
    p = Product.objects.create(customer=c, sku="SKU-2", name="Producto 2")

    m = record_movement(MovementInput(MovementType.IN, w.id, p.id, 1))
    assert m.pdf
    assert m.pdf.name.endswith(".pdf")
