from django.db import models

class Stock(models.Model):
    warehouse = models.ForeignKey("locations.Warehouse", on_delete=models.PROTECT, related_name="stocks")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["warehouse", "product"], name="uniq_stock_warehouse_product")
        ]

    def __str__(self):
        return f"{self.warehouse} | {self.product} = {self.quantity}"
