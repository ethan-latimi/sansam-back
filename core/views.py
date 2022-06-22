from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import EmptyPage, PageNotAnInteger
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/accounts/',
        '/api/customers/',
        '/api/farms/',
        '/api/orders/',
        '/api/products/',
        '/api/todos/',
        '/api/users/',
    ]
    return Response(routes)


def pagination(page, paginator):
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
