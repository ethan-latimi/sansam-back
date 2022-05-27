# Django
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.views import pagination

from customers.models import Customer
from customers.serializers import CustomerSerializer


# 고객 전체 보기
# (고객 정보를 이용하여 검색): 이름, 매출정렬(false=낮은, true=높은)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCustomer(request):
    user = request.user
    query = request.query_params.get('keyword')
    order = request.query_params.get('order')
    if order == None:
        order = 'false'
    if query == None:
        query = ''
    page = request.query_params.get('page')
    if order.lower() == 'false':
        customers = Customer.objects.filter(
            owner=user, name__icontains=query).order_by('totalSpend')
    elif order.lower() == 'true':
        customers = Customer.objects.filter(
            owner=user, name__icontains=query).order_by('-totalSpend')
    paginator = Paginator(customers, 10)
    customers = pagination(page, paginator)
    serializer = CustomerSerializer(customers, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
# 고객 입력

# 고객 수정

# 고객 매출 순위

# 고객 소개자 순위
