from rest_framework import serializers
from apps.inventory.models import Stock, Movement
from apps.inventory.services import MovementInput, InsufficientStock, record_movement

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "warehouse", "product", "quantity", "updated_at"]
        read_only_fields = fields

class MovementSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Movement
        fields = ["id", "movement_type", "warehouse", "product", "quantity", "stock_before", "stock_after", "occurred_at", "pdf", "pdf_url"]
        read_only_fields = fields

    def get_pdf_url(self, obj):
        if not obj.pdf:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pdf.url) if request else obj.pdf.url

class MovementCreateSerializer(serializers.Serializer):
    movement_type = serializers.ChoiceField(choices=["IN", "OUT"])
    warehouse_id = serializers.IntegerField(min_value=1)
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        data = MovementInput(
            movement_type=validated_data["movement_type"],
            warehouse_id=validated_data["warehouse_id"],
            product_id=validated_data["product_id"],
            quantity=validated_data["quantity"],
        )
        try:
            return record_movement(data)
        except InsufficientStock as e:
            raise serializers.ValidationError(
                {"quantity": [{"message": str(e), "available": e.available, "requested": e.requested}]}
            )
