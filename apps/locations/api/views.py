from rest_framework.viewsets import ModelViewSet
from apps.locations.models import Branch, Warehouse
from .serializers import BranchSerializer, WarehouseSerializer

class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer

    def get_queryset(self):
        qs = Branch.objects.all()
        customer_id = self.request.query_params.get("customer_id")
        return qs.filter(customer_id=customer_id) if customer_id else qs

class WarehouseViewSet(ModelViewSet):
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        qs = Warehouse.objects.all()
        branch_id = self.request.query_params.get("branch_id")
        return qs.filter(branch_id=branch_id) if branch_id else qs
