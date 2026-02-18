from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from apps.customers.models import Customer
from apps.locations.models import Branch
from .forms import BranchForm

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

    def get_initial(self):
        initial = super().get_initial()
        customer_id = (self.request.GET.get("customer_id") or "").strip()
        if customer_id.isdigit():
            initial["customer"] = int(customer_id)
        return initial

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
