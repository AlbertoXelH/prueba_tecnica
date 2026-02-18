from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, WarehouseViewSet

router = DefaultRouter()
router.register(r"branches", BranchViewSet, basename="branches")
router.register(r"warehouses", WarehouseViewSet, basename="warehouses")

urlpatterns = router.urls
