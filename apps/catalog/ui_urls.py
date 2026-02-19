from django.urls import path
from .ui_views import ProductCreateView, ProductListView, ProductUpdateView, product_toggle_active
from .ui_api import products_by_customer

urlpatterns = [
    path("productos/", ProductListView.as_view(), name="products_list"),
    path("productos/nuevo/", ProductCreateView.as_view(), name="products_create"),
    path("productos/<int:pk>/editar/", ProductUpdateView.as_view(), name="products_edit"),
    path("productos/<int:pk>/estado/", product_toggle_active, name="products_toggle"),
    path("ui/products/", products_by_customer, name="products_by_customer"),
]

