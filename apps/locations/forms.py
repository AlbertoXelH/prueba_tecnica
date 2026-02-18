from django import forms
from apps.locations.models import Branch

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["customer", "name", "code", "address", "city", "state", "is_active"]
        labels = {
            "customer": "Cliente",
            "name": "Nombre",
            "code": "Código",
            "address": "Dirección",
            "city": "Ciudad",
            "state": "Estado",
            "is_active": "Activo",
        }
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Centro"}),
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. BR-001"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Calle y número"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ciudad"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "Estado"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
