from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from apps.customers.models import Customer
from apps.locations.models import Branch, Warehouse
from .forms import WarehouseForm

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

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["customers"] = Customer.objects.order_by("name")
        ctx["branches"] = Branch.objects.select_related("customer").order_by("customer__name", "name")
        return ctx

class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "ui/warehouses/form.html"

    def get_initial(self):
        initial = super().get_initial()
        branch_id = (self.request.GET.get("branch_id") or "").strip()
        if branch_id.isdigit():
            initial["branch"] = int(branch_id)
        return initial

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
