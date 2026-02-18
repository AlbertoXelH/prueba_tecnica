from rest_framework import serializers
from apps.locations.models import Branch, Warehouse

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "customer", "name", "code", "address", "city", "state", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "branch", "name", "code", "address", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
