from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, ListView

from apps.inventory.models import Movement
from apps.inventory.services import InsufficientStock, MovementInput, record_movement
from .forms import MovementForm

class MovementListView(ListView):
    model = Movement
    template_name = "ui/movements/list.html"
    context_object_name = "movements"
    paginate_by = 20

    def get_queryset(self):
        return (
            Movement.objects.select_related("warehouse__branch__customer", "product")
            .all()
            .order_by("-occurred_at")
        )

class MovementCreateView(FormView):
    template_name = "ui/movements/form.html"
    form_class = MovementForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        customer_id = (self.request.POST.get("customer") or self.request.GET.get("customer") or "").strip()
        branch_id = (self.request.POST.get("branch") or self.request.GET.get("branch") or "").strip()
        kwargs["customer_id"] = int(customer_id) if customer_id.isdigit() else None
        kwargs["branch_id"] = int(branch_id) if branch_id.isdigit() else None
        return kwargs

    def form_valid(self, form):
        data = MovementInput(
            movement_type=form.cleaned_data["movement_type"],
            warehouse_id=form.cleaned_data["warehouse"].id,
            product_id=form.cleaned_data["product"].id,
            quantity=form.cleaned_data["quantity"],
        )
        try:
            record_movement(data)
        except InsufficientStock as e:
            form.add_error("quantity", f"Stock insuficiente. Disponible: {e.available}, solicitado: {e.requested}.")
            return self.form_invalid(form)

        messages.success(self.request, "Movimiento registrado correctamente.")
        return redirect("ui:movements_list")

    def get_success_url(self):
        return reverse("ui:movements_list")

def movement_pdf(request, pk):
    m = Movement.objects.filter(pk=pk).first()
    if not m or not m.pdf:
        raise Http404("PDF no disponible")

    f = m.pdf.open("rb")
    filename = f"comprobante_{m.id}.pdf"
    return FileResponse(f, as_attachment=True, filename=filename)
