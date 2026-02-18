from rest_framework.viewsets import ModelViewSet
from apps.customers.models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
