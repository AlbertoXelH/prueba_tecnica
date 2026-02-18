from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from apps.customers.models import Customer
from .forms import CustomerForm

class CustomerListView(ListView):
    model = Customer
    template_name = "ui/customers/list.html"
    context_object_name = "customers"
    paginate_by = 20

    def get_queryset(self):
        qs = Customer.objects.all()
        q = (self.request.GET.get("q") or "").strip()
        status = (self.request.GET.get("status") or "").strip()
        if q:
            qs = qs.filter(name__icontains=q)
        if status == "active":
            qs = qs.filter(is_active=True)
        if status == "inactive":
            qs = qs.filter(is_active=False)
        return qs

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "ui/customers/form.html"

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Cliente creado correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:customers_list")

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "ui/customers/form.html"

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Cliente actualizado correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:customers_list")

def customer_toggle_active(request, pk: int):
    c = get_object_or_404(Customer, pk=pk)
    c.is_active = not c.is_active
    c.save(update_fields=["is_active", "updated_at"])
    messages.success(request, "Estado actualizado.")
    return redirect("ui:customers_list")
