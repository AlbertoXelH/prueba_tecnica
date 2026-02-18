from django.urls import path
from .ui_views import CustomerListView, CustomerCreateView, CustomerUpdateView, customer_toggle_active

urlpatterns = [
    path("clientes/", CustomerListView.as_view(), name="customers_list"),
    path("clientes/nuevo/", CustomerCreateView.as_view(), name="customers_create"),
    path("clientes/<int:pk>/editar/", CustomerUpdateView.as_view(), name="customers_edit"),
    path("clientes/<int:pk>/estado/", customer_toggle_active, name="customers_toggle"),
]
