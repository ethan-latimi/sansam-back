from django.urls import path
from . import views

urlpatterns = [
    path('', views.getOrderList, name='order-list'),
]
