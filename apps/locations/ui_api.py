from django.http import JsonResponse
from django.views.decorators.http import require_GET

from apps.locations.models import Branch, Warehouse


@require_GET
def branches_by_customer(request):
    customer_id = (request.GET.get("customer_id") or "").strip()
    qs = Branch.objects.order_by("name")
    if customer_id.isdigit():
        qs = qs.filter(customer_id=int(customer_id))
    data = [{"id": b.id, "name": b.name} for b in qs]
    return JsonResponse({"results": data})


@require_GET
def warehouses_by_branch(request):
    branch_id = (request.GET.get("branch_id") or "").strip()
    qs = Warehouse.objects.order_by("name")
    if branch_id.isdigit():
        qs = qs.filter(branch_id=int(branch_id))
    data = [{"id": w.id, "name": w.name} for w in qs]
    return JsonResponse({"results": data})
