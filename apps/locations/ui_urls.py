from django.urls import path

from .ui_api import branches_by_customer, warehouses_by_branch
from .ui_views import BranchCreateView, BranchListView, BranchUpdateView, branch_toggle_active

urlpatterns = [
    # UI sucursales
    path("sucursales/", BranchListView.as_view(), name="branches_list"),
    path("sucursales/nueva/", BranchCreateView.as_view(), name="branches_create"),
    path("sucursales/<int:pk>/editar/", BranchUpdateView.as_view(), name="branches_edit"),
    path("sucursales/<int:pk>/estado/", branch_toggle_active, name="branches_toggle"),

    # JSON para selects dependientes (UI)
    path("ui/branches/", branches_by_customer, name="ui_branches_by_customer"),
    path("ui/warehouses/", warehouses_by_branch, name="ui_warehouses_by_branch"),
]
