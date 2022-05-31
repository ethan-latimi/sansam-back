from django.urls import path
from . import views

urlpatterns = [
    path('', views.getCustomerList, name='customer'),
    path('<str:pk>', views.getCustomer, name='customer-list'),
    path('create/', views.postCustomer, name='post-customer'),
    path('update/', views.putCustomer, name='put-customer'),
    path('delete/', views.deleteCustomer, name='delete-customer'),
]
