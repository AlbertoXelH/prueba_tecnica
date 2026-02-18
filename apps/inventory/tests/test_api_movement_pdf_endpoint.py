import pytest
from django.urls import reverse

from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from apps.catalog.models import Product
from apps.inventory.models import MovementType
from apps.inventory.services import MovementInput, record_movement

pytestmark = pytest.mark.django_db


def test_api_movement_pdf_endpoint(client):
    c = Customer.objects.create(name="ACME")
    b = Branch.objects.create(customer=c, name="Centro")
    w = Warehouse.objects.create(branch=b, name="Principal")
    p = Product.objects.create(customer=c, sku="SKU-API", name="Producto API")

    m = record_movement(MovementInput(MovementType.IN, w.id, p.id, 1))

    # endpoint API ya lo tienes funcionando: /api/movements/<uuid>/pdf/
    url = f"/api/movements/{m.id}/pdf/"
    r = client.get(url)
    assert r.status_code == 200
    assert r["Content-Type"] in ("application/pdf", "application/octet-stream")
