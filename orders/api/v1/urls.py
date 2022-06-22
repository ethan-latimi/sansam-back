from django.urls import path
from . import views


urlpatterns = [
    path('', views.getOrderList, name='order-list'),
    path('create/', views.postOrder, name='createOrder'),
    path('update/<str:pk>', views.putOrder, name="putOrder"),
    path('delete/<str:pk>', views.deleteOrder, name="deleteOrder"),
    path('orderItem/create/', views.postOrderItem, name="postOrderItem"),
    path('orderImage/create/<str:pk>',
         views.postOrderImage, name="postOrderImage"),
    path('orderItems/<str:pk>', views.getOrderItems, name="orderItems"),
    path('orderImages/<str:pk>',
         views.getOrderImages, name="orderImages"),
]
