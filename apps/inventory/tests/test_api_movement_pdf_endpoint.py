import pytest
from rest_framework.test import APIClient
from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from apps.catalog.models import Product
from apps.inventory.models import MovementType
from apps.inventory.services import MovementInput, record_movement

pytestmark = pytest.mark.django_db

def test_api_can_download_movement_pdf():
    c = Customer.objects.create(name="ACME")
    b = Branch.objects.create(customer=c, name="Centro")
    w = Warehouse.objects.create(branch=b, name="Principal")
    p = Product.objects.create(sku="SKU-API", name="Producto API")

    m = record_movement(MovementInput(MovementType.IN, w.id, p.id, 1))

    client = APIClient()
    r = client.get(f"/api/movements/{m.id}/pdf/")
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/pdf"
