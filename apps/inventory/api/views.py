from django.http import FileResponse
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from apps.inventory.models import Stock, Movement
from .serializers import StockSerializer, MovementSerializer, MovementCreateSerializer

class StockViewSet(ReadOnlyModelViewSet):
    serializer_class = StockSerializer

    def get_queryset(self):
        qs = Stock.objects.select_related("warehouse", "product").all()
        warehouse_id = self.request.query_params.get("warehouse_id")
        product_id = self.request.query_params.get("product_id")
        if warehouse_id:
            qs = qs.filter(warehouse_id=warehouse_id)
        if product_id:
            qs = qs.filter(product_id=product_id)
        return qs

class MovementViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Movement.objects.select_related("warehouse", "product").all()

    def get_serializer_class(self):
        return MovementCreateSerializer if self.action == "create" else MovementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movement = serializer.save()
        return Response(MovementSerializer(movement, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def pdf(self, request, pk=None):
        movement = self.get_object()
        if not movement.pdf:
            return Response({"detail": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)
        return FileResponse(movement.pdf.open("rb"), content_type="application/pdf", as_attachment=True, filename=f"{movement.id}.pdf")
