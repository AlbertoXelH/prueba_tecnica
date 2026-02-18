from django.urls import path, include

urlpatterns = [
    path("", include("apps.customers.api.urls")),
    path("", include("apps.locations.api.urls")),
    path("", include("apps.catalog.api.urls")),
    path("", include("apps.inventory.api.urls")),
]
