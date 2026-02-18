from django.db import transaction
from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from apps.catalog.models import Product
from apps.inventory.models import Stock

@transaction.atomic
def seed():
    # Limpia por si acaso (deja vacío)
    Stock.objects.all().delete()
    Warehouse.objects.all().delete()
    Branch.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()

    customers = [
        ("ACME", "ACM-0001", "contacto@acme.com", "5511111111"),
        ("PepsiCo", "PEP-0001", "contacto@pepsico.com", "5522222222"),
        ("Bimbo", "BIM-0001", "contacto@bimbo.com", "5533333333"),
    ]

    for cname, rfc, email, phone in customers:
        c = Customer.objects.create(
            name=cname,
            tax_id=rfc,
            email=email,
            phone=phone,
            is_active=True,
        )

        # 2 sucursales por cliente
        branches = []
        for i in range(1, 3):
            b = Branch.objects.create(
                customer=c,
                name=f"{cname} - Sucursal {i}",
                code=f"{cname[:3].upper()}-BR-{i:02d}",
                address=f"Calle {i} #{100+i}",
                city="Ciudad de México",
                state="CDMX",
                is_active=True,
            )
            branches.append(b)

        # 2 almacenes por sucursal
        for b in branches:
            for j in range(1, 3):
                Warehouse.objects.create(
                    branch=b,
                    name=f"{b.name} - Almacén {j}",
                    code=f"{b.code}-WH-{j:02d}",
                    address=f"Bodega {j}, {b.address}",
                    is_active=True,
                )

        # 4 productos por cliente
        for k in range(1, 5):
            Product.objects.create(
                customer=c,
                sku=f"{cname[:3].upper()}-SKU-{k:03d}",
                name=f"Producto {k} ({cname})",
                description=f"Descripción del producto {k} de {cname}",
                unit="pz",
                is_active=True,
            )

seed()

print("OK seed terminado")
print("Customers:", Customer.objects.count())
print("Branches:", Branch.objects.count())
print("Warehouses:", Warehouse.objects.count())
print("Products:", Product.objects.count())
print("Stocks:", Stock.objects.count())
