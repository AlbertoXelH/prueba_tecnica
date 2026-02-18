from django.db import models


class Warehouse(models.Model):
    branch = models.ForeignKey(
        "locations.Branch",
        on_delete=models.PROTECT,
        related_name="warehouses",
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=60)
    address = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["branch__customer__name", "branch__name", "name"]

    def __str__(self):
        return f"{self.branch.name} - {self.name}"
