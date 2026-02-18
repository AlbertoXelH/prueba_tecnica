from django import forms
from apps.catalog.models import Product
from apps.customers.models import Customer


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["customer", "sku", "name", "description", "unit", "is_active"]
        labels = {
            "customer": "Cliente",
            "sku": "SKU",
            "name": "Nombre",
            "description": "Descripción",
            "unit": "Unidad",
            "is_active": "Activo",
        }
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. SKU-001"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Agua 600ml"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción (opcional)"}),
            "unit": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. pza / caja / kg"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].queryset = Customer.objects.order_by("name")
