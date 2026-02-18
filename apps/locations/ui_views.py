from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from .forms import BranchForm, WarehouseForm


# -------------------------
# Sucursales
# -------------------------
class BranchListView(ListView):
    model = Branch
    template_name = "ui/branches/list.html"
    context_object_name = "branches"
    paginate_by = 20

    def get_queryset(self):
        qs = Branch.objects.select_related("customer").all()
        customer_id = (self.request.GET.get("customer_id") or "").strip()
        q = (self.request.GET.get("q") or "").strip()
        status = (self.request.GET.get("status") or "").strip()

        if customer_id.isdigit():
            qs = qs.filter(customer_id=int(customer_id))
        if q:
            qs = qs.filter(name__icontains=q)
        if status == "active":
            qs = qs.filter(is_active=True)
        if status == "inactive":
            qs = qs.filter(is_active=False)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["customers"] = Customer.objects.order_by("name")
        return ctx


class BranchCreateView(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = "ui/branches/form.html"

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Sucursal creada correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:branches_list")


class BranchUpdateView(UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = "ui/branches/form.html"

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Sucursal actualizada correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:branches_list")


def branch_toggle_active(request, pk: int):
    b = get_object_or_404(Branch, pk=pk)
    b.is_active = not b.is_active
    b.save(update_fields=["is_active", "updated_at"])
    messages.success(request, "Estado actualizado.")
    return redirect("ui:branches_list")


# -------------------------
# Almacenes
# -------------------------
class WarehouseListView(ListView):
    model = Warehouse
    template_name = "ui/warehouses/list.html"
    context_object_name = "warehouses"
    paginate_by = 20

    def get_queryset(self):
        qs = Warehouse.objects.select_related("branch__customer").all()
        customer_id = (self.request.GET.get("customer_id") or "").strip()
        branch_id = (self.request.GET.get("branch_id") or "").strip()
        q = (self.request.GET.get("q") or "").strip()
        status = (self.request.GET.get("status") or "").strip()

        if customer_id.isdigit():
            qs = qs.filter(branch__customer_id=int(customer_id))
        if branch_id.isdigit():
            qs = qs.filter(branch_id=int(branch_id))
        if q:
            qs = qs.filter(name__icontains=q)
        if status == "active":
            qs = qs.filter(is_active=True)
        if status == "inactive":
            qs = qs.filter(is_active=False)

        return qs.order_by("branch__customer__name", "branch__name", "name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["customers"] = Customer.objects.order_by("name")
        # para el filtro de sucursal (si ya eligieron cliente, puedes filtrar en template con JS,
        # pero aquí al menos mandamos todas, la UI puede refinarlo luego)
        ctx["branches"] = Branch.objects.select_related("customer").order_by("customer__name", "name")
        return ctx


class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "ui/warehouses/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        customer_id = (self.request.POST.get("customer") or self.request.GET.get("customer") or "").strip()
        kwargs["customer_id"] = int(customer_id) if customer_id.isdigit() else None
        return kwargs

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Almacén creado correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:warehouses_list")


class WarehouseUpdateView(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "ui/warehouses/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # al editar, el form ya infiere customer desde la sucursal,
        # pero si viene customer en query lo respetamos para recargar combos
        customer_id = (self.request.POST.get("customer") or self.request.GET.get("customer") or "").strip()
        kwargs["customer_id"] = int(customer_id) if customer_id.isdigit() else None
        return kwargs

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Almacén actualizado correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:warehouses_list")


def warehouse_toggle_active(request, pk: int):
    w = get_object_or_404(Warehouse, pk=pk)
    w.is_active = not w.is_active
    w.save(update_fields=["is_active", "updated_at"])
    messages.success(request, "Estado actualizado.")
    return redirect("ui:warehouses_list")
