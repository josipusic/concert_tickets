from django.urls import path
from .views import create_ticket


urlpatterns = [
    path('ticket/create/', create_ticket, name='create-ticket'),
]
