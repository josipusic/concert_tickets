from django.urls import path

from .views import CustomerDetailAPIView, get_related_tickets


urlpatterns = [
    path('customer/', CustomerDetailAPIView.as_view(), name='customer'),
    path('customer/tickets/', get_related_tickets),
]
