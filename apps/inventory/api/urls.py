from rest_framework.routers import DefaultRouter
from .views import StockViewSet, MovementViewSet

router = DefaultRouter()
router.register(r"stocks", StockViewSet, basename="stocks")
router.register(r"movements", MovementViewSet, basename="movements")

urlpatterns = router.urls
