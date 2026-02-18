from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.catalog.models import Product

@require_GET
def products_by_customer(request):
    customer_id = (request.GET.get("customer_id") or "").strip()
    qs = Product.objects.order_by("sku")
    if customer_id.isdigit():
        qs = qs.filter(customer_id=int(customer_id))
    data = [{"id": p.id, "name": str(p)} for p in qs]
    return JsonResponse({"results": data})
