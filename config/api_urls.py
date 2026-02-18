from rest_framework.routers import DefaultRouter
from apps.customers.api.views import CustomerViewSet
from apps.locations.api.views import BranchViewSet, WarehouseViewSet
from apps.catalog.api.views import ProductViewSet
from apps.inventory.api.views import StockViewSet, MovementViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"branches", BranchViewSet, basename="branches")
router.register(r"warehouses", WarehouseViewSet, basename="warehouses")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"stocks", StockViewSet, basename="stocks")
router.register(r"movements", MovementViewSet, basename="movements")

urlpatterns = router.urls
