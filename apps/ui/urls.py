from django.urls import include, path
from .views import HomeView

app_name = "ui"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("", include("apps.customers.ui_urls")),
    path("", include("apps.locations.ui_urls")),
]
