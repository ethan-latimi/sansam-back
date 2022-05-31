from django.urls import path
from . import views

urlpatterns = [
    path('', views.getTodoList, name='todos'),
    path('todo/<str:pk>/', views.getTodo, name='todo'),
    path('create/', views.postTodo, name='create-todo'),
    path('update/', views.putTodo, name='update-todo'),
    path('delete/', views.deleteTodo, name='delete-todo'),
]
