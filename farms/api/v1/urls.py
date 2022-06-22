from django.urls import path
from . import views

urlpatterns = [
    # farm
    path('', views.getFarmList, name='farm-list'),
    path('farm/upload/<str:pk>/', views.uploadFarmImage, name='upload-farm-image'),
    path('farm/<str:pk>/', views.getFarm, name="farm"),
    path('create/', views.postFarm, name='post-farm'),
    path('update/<str:pk>/', views.putFarm, name='update-farm'),
    path('delete/<str:pk>/',
         views.deleteFarm, name='delete-farm'),
    # log
    path('logs/<str:farm_pk>/', views.getLogList, name='log-list'),
    path('log/upload/<str:log_pk>/',
         views.uploadLogImage, name='upload-farm-image'),
    path('log/<str:log_pk>/', views.getLog, name='log'),
    path('log/create/<str:farm_pk>/', views.postLog, name='post-log'),
    path('log/update/<str:log_pk>/', views.putLog, name='put-log'),
    path('log/delete/<str:log_pk>/', views.deleteLog, name='delete-log'),
]
