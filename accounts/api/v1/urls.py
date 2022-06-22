from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAccount, name='account'),
    path('dashboard/', views.getDashboard, name="dashboard"),
    path('transactions/', views.getTransaction, name="transactions"),
    path('transactions/create/', views.postTransaction, name='post-transaction'),
    path('transactions/update/<str:pk>/',
         views.putTransaction, name='put-transaction'),
    path('transactions/delete/<str:pk>/',
         views.deleteTransaction, name='delete-transaction'),
]
