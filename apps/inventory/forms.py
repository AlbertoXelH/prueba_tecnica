from django import forms

from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from apps.catalog.models import Product
from apps.inventory.models import MovementType


class MovementForm(forms.Form):
    movement_type = forms.ChoiceField(
        choices=MovementType.choices,
        label="Tipo de movimiento",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.order_by("name"),
        label="Cliente",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    branch = forms.ModelChoiceField(
        queryset=Branch.objects.none(),
        label="Sucursal",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.none(),
        label="Almacén",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by("name"),
        label="Producto",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    quantity = forms.IntegerField(
        min_value=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ej. 10"}),
    )

    def __init__(self, *args, **kwargs):
        customer_id = kwargs.pop("customer_id", None)
        branch_id = kwargs.pop("branch_id", None)
        super().__init__(*args, **kwargs)

        if customer_id:
            self.fields["branch"].queryset = Branch.objects.filter(customer_id=customer_id).order_by("name")

        if branch_id:
            self.fields["warehouse"].queryset = Warehouse.objects.filter(branch_id=branch_id).order_by("name")
