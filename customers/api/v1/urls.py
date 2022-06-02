from django.urls import path
from . import views

urlpatterns = [
    path('', views.getCustomerList, name='customer'),
    path('<str:pk>', views.getCustomer, name='customer-list'),
    path('create/', views.postCustomer, name='post-customer'),
    path('update/<str:pk>', views.putCustomer, name='put-customer'),
    path('delete/<str:pk>', views.deleteCustomer, name='delete-customer'),
]
