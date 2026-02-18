from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.locations.models import Branch


@require_GET
def branches_by_customer(request):
    customer_id = (request.GET.get("customer_id") or "").strip()
    qs = Branch.objects.order_by("name")
    if customer_id.isdigit():
        qs = qs.filter(customer_id=int(customer_id))
    data = [{"id": b.id, "name": b.name} for b in qs]
    return JsonResponse({"results": data})
