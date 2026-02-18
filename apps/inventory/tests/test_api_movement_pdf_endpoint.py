import pytest
from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from apps.catalog.models import Product
from apps.inventory.models import MovementType
from apps.inventory.services import MovementInput, record_movement

pytestmark = pytest.mark.django_db


def test_api_movement_pdf_endpoint(client):
    c = Customer.objects.create(
        name="ACME",
        tax_id="XAXX010101000",
        email="acme@example.com",
        phone="5555555555",
    )
    b = Branch.objects.create(
        customer=c,
        name="Centro",
        code="BR-001",
        address="Calle 1 #123",
        city="CDMX",
        state="CDMX",
    )
    w = Warehouse.objects.create(
        branch=b,
        name="Principal",
        code="WH-001",
        address="Bodega 10",
    )
    p = Product.objects.create(
        customer=c,
        sku="SKU-API",
        name="Producto API",
        description="Desc API",
        unit="pz",
    )

    m = record_movement(MovementInput(MovementType.IN, w.id, p.id, 1))

    url = f"/api/movements/{m.id}/pdf/"
    r = client.get(url)
    assert r.status_code == 200
    assert r["Content-Type"] in ("application/pdf", "application/octet-stream")
