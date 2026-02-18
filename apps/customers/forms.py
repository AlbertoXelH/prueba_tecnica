from django import forms
from apps.customers.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "tax_id", "email", "phone", "is_active"]
        labels = {
            "name": "Nombre",
            "tax_id": "RFC",
            "email": "Correo",
            "phone": "Teléfono",
            "is_active": "Activo",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. ACME"}),
            "tax_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. XAXX010101000"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@dominio.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. 55 1234 5678"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
