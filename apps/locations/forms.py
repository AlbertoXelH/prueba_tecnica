from django import forms
from apps.customers.models import Customer
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
    # Campo extra (NO existe en el modelo) para filtrar sucursales por cliente.
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.order_by("name"),
        label="Cliente",
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Warehouse
        fields = ["branch", "name", "code", "address", "is_active"]
        labels = {
            "branch": "Sucursal",
            "name": "Nombre",
            "code": "Código",
            "address": "Dirección",
            "is_active": "Activo",
        }
        widgets = {
            "branch": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Almacén principal"}),
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. WH-001"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Calle y número"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        customer_id = kwargs.pop("customer_id", None)
        super().__init__(*args, **kwargs)

        # Si estamos editando, inferimos el cliente desde la sucursal del almacén.
        if self.instance and getattr(self.instance, "pk", None):
            inferred_customer = self.instance.branch.customer
            self.fields["customer"].initial = inferred_customer.pk
            self.fields["branch"].queryset = Branch.objects.filter(customer=inferred_customer).order_by("name")
        else:
            # Alta: no permitimos escoger sucursal hasta elegir cliente.
            self.fields["branch"].queryset = Branch.objects.none()

        if customer_id:
            self.fields["customer"].initial = customer_id
            self.fields["branch"].queryset = Branch.objects.filter(customer_id=customer_id).order_by("name")

    def clean(self):
        cleaned = super().clean()
        customer = cleaned.get("customer")
        branch = cleaned.get("branch")

        if customer and branch and branch.customer_id != customer.id:
            self.add_error("branch", "La sucursal seleccionada no pertenece al cliente.")
        return cleaned
