from django.db import models


class Branch(models.Model):
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="branches",
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=60)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["customer__name", "name"]

    def __str__(self):
        return f"{self.customer.name} - {self.name}"
