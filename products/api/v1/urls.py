from django.urls import path
from . import views

urlpatterns = [
    path('', views.getProductList, name='products'),
    path('product/<str:pk>/', views.getProduct, name='product'),
    path('create/', views.postProduct, name='create-product'),
    path('update/<str:pk>/', views.putProduct, name='update-product'),
    path('updateQty/<str:pk>/', views.putProductQty, name='update-product'),
    path('delete/<str:pk>/', views.deleteProduct, name='delete-product'),
    path('categories/', views.getCategoryList, name='categories'),
    path('categories/create/', views.postCategory, name='create-category'),
    path('categories/update/<str:pk>/',
         views.putCategory, name='update-category'),
    path('categories/delete/<str:pk>/',
         views.deleteCategory, name='delete-category'),
]
