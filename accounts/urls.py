from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAccount, name='account'),
    path('transactions/', views.getTransaction, name="transactions"),
    path('transactions/post/', views.postTransaction, name='post-transaction'),
    path('transactions/delete/<str:pk>/',
         views.deleteTransaction, name='delete-transaction'),
]
