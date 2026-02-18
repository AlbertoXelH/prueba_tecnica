from django import forms
from apps.locations.models import Branch, Warehouse


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


class WarehouseForm(forms.ModelForm):
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.select_related("customer").order_by("customer__name", "name"),
        label="Sucursal",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Warehouse
        fields = ["branch", "name", "code", "address", "is_active"]
        labels = {
            "name": "Nombre",
            "code": "Código",
            "address": "Dirección",
            "is_active": "Activo",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Principal"}),
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. WH-001"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Calle y número"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Etiqueta más clara: "Cliente - Sucursal"
        self.fields["branch"].label_from_instance = lambda b: f"{b.customer.name} - {b.name}"
