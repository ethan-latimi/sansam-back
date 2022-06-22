"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_url_patterns = [
    path('api/v1/users/', include('users.api.v1.urls')),
    path('api/v1/accounts/', include('accounts.api.v1.urls')),
    path('api/v1/customers/', include('customers.api.v1.urls')),
    path('api/v1/farms/', include('farms.api.v1.urls')),
    path('api/v1/orders/', include('orders.api.v1.urls')),
    path('api/v1/products/', include('products.api.v1.urls')),
    path('api/v1/todos/', include('todos.api.v1.urls')),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Open API",
        default_version='v1',
        description='''
        # API 문서:
        ### (산삼 농장: sansam88.com)
        --- 
        산삼 농장 관리 시스템을 웹앱으로 반영하여 만든 Managing System Webapp,
        DRF Django 이용
         
        작성자: 조민수
        Organization: Latimi-Sauce
        ''',
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)


urlpatterns = [
    path('api/', include('core.urls')),
    path('api/v1/users/', include('users.api.v1.urls')),
    path('api/v1/accounts/', include('accounts.api.v1.urls')),
    path('api/v1/customers/', include('customers.api.v1.urls')),
    path('api/v1/farms/', include('farms.api.v1.urls')),
    path('api/v1/orders/', include('orders.api.v1.urls')),
    path('api/v1/products/', include('products.api.v1.urls')),
    path('api/v1/todos/', include('todos.api.v1.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger',
                                                  cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc',
                                                cache_timeout=0), name='schema-redoc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
