import uuid
from django.core.validators import MinValueValidator
from django.db import models

class MovementType(models.TextChoices):
    IN = "IN", "Ingreso"
    OUT = "OUT", "Egreso"

class Movement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movement_type = models.CharField(max_length=3, choices=MovementType.choices)
    warehouse = models.ForeignKey("locations.Warehouse", on_delete=models.PROTECT, related_name="movements")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT, related_name="movements")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    stock_before = models.PositiveIntegerField()
    stock_after = models.PositiveIntegerField()
    occurred_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="documents/movements/%Y/%m/%d/", blank=True, null=True)

    class Meta:
        ordering = ["-occurred_at"]

    def __str__(self):
        return f"{self.movement_type} {self.product} x{self.quantity} @ {self.warehouse}"
