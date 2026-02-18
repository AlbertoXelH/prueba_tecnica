from django import forms
from apps.catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["sku", "name", "description", "unit", "is_active"]
        labels = {
            "sku": "SKU",
            "name": "Nombre",
            "description": "Descripción",
            "unit": "Unidad",
            "is_active": "Activo",
        }
        widgets = {
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. SKU-001"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Producto X"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción breve"}),
            "unit": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. pza, kg, caja"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
