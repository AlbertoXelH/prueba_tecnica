from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.db.models import Q

from apps.catalog.models import Product
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = "ui/products/list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.all().order_by("name")
        q = (self.request.GET.get("q") or "").strip()
        status = (self.request.GET.get("status") or "").strip()

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(sku__icontains=q))

        if status == "active":
            qs = qs.filter(is_active=True)
        if status == "inactive":
            qs = qs.filter(is_active=False)

        return qs


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "ui/products/form.html"

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Producto creado correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "ui/products/form.html"

    def form_valid(self, form):
        r = super().form_valid(form)
        messages.success(self.request, "Producto actualizado correctamente.")
        return r

    def get_success_url(self):
        return reverse("ui:products_list")


def product_toggle_active(request, pk: int):
    p = get_object_or_404(Product, pk=pk)
    p.is_active = not p.is_active
    p.save(update_fields=["is_active", "updated_at"])
    messages.success(request, "Estado actualizado.")
    return redirect("ui:products_list")
