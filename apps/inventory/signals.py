from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.catalog.models import Product
from apps.inventory.models import Stock
from apps.locations.models import Warehouse


@receiver(post_save, sender=Product)
def create_zero_stock_for_new_product(sender, instance: Product, created: bool, **kwargs):
    """
    Cuando se crea un producto de un cliente, se crea Stock(quantity=0)
    para todos los almacenes de todas las sucursales de ese cliente.
    """
    if not created:
        return

    warehouses = Warehouse.objects.filter(branch__customer_id=instance.customer_id).only("id")
    rows = [
        Stock(warehouse_id=w.id, product_id=instance.id, quantity=0)
        for w in warehouses
    ]
    if rows:
        Stock.objects.bulk_create(rows, ignore_conflicts=True)


@receiver(post_save, sender=Warehouse)
def create_zero_stock_for_new_warehouse(sender, instance: Warehouse, created: bool, **kwargs):
    """
    Cuando se crea un almacén, se crea Stock(quantity=0) para
    todos los productos del cliente dueño de la sucursal.
    """
    if not created:
        return

    customer_id = instance.branch.customer_id
    products = Product.objects.filter(customer_id=customer_id).only("id")
    rows = [
        Stock(warehouse_id=instance.id, product_id=p.id, quantity=0)
        for p in products
    ]
    if rows:
        Stock.objects.bulk_create(rows, ignore_conflicts=True)
