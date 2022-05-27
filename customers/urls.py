from django.urls import path
from . import views

urlpatterns = [
    path('', views.getCustomer, name='customer'),
]
