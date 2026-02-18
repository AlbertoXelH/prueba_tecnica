from django.db import models

class Product(models.Model):
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="products",
    )
    sku = models.CharField(max_length=80)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["customer__name", "sku"]
        constraints = [
            models.UniqueConstraint(fields=["customer", "sku"], name="uniq_product_customer_sku")
        ]

    def __str__(self):
        return f"{self.sku} - {self.name}"
