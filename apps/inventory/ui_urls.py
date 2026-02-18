from django.urls import path
from .ui_views import MovementCreateView, MovementListView, movement_pdf

urlpatterns = [
    path("movimientos/", MovementListView.as_view(), name="movements_list"),
    path("movimientos/nuevo/", MovementCreateView.as_view(), name="movements_create"),
    path("movimientos/<uuid:pk>/pdf/", movement_pdf, name="movements_pdf"),
]
