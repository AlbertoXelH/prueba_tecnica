from django.urls import path

from .ui_api import branches_by_customer
from .ui_views import (
    BranchCreateView, BranchListView, BranchUpdateView, branch_toggle_active,
    WarehouseCreateView, WarehouseListView, WarehouseUpdateView, warehouse_toggle_active
)

urlpatterns = [
    # Sucursales
    path("sucursales/", BranchListView.as_view(), name="branches_list"),
    path("sucursales/nueva/", BranchCreateView.as_view(), name="branches_create"),
    path("sucursales/<int:pk>/editar/", BranchUpdateView.as_view(), name="branches_edit"),
    path("sucursales/<int:pk>/estado/", branch_toggle_active, name="branches_toggle"),

    # Almacenes
    path("almacenes/", WarehouseListView.as_view(), name="warehouses_list"),
    path("almacenes/nuevo/", WarehouseCreateView.as_view(), name="warehouses_create"),
    path("almacenes/<int:pk>/editar/", WarehouseUpdateView.as_view(), name="warehouses_edit"),
    path("almacenes/<int:pk>/estado/", warehouse_toggle_active, name="warehouses_toggle"),

    # UI API (para selects dependientes)
    path("ui/branches/", branches_by_customer, name="ui_branches_by_customer"),
]
