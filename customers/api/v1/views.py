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
def getCustomerList(request):
    user = request.user
    query = request.query_params.get('keyword')
    order = request.query_params.get('order')
    if order == None:
        order = 'true'
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


# 고객 한명 보기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCustomer(request, pk):
    user = request.user
    customer = Customer.objects.get(id=pk)
    if user == customer.owner:
        serializer = CustomerSerializer(customer, many=False)
        return Response({'result': serializer.data})
    else:
        return Response("해당하는 고객이 없습니다.")


# 고객 입력 (고객 전체보기를 통해 고객의 아이디를 reference에 넣어줍니다.)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postCustomer(request):
    user = request.user
    data = request.data
    try:
        customer = Customer.objects.create(
            name=data['name'],
            address=data['address'],
            email=data['email'],
            phoneNumber=data['phoneNumber'],
            secondPhoneNumber=data['secondPhoneNumber'],
            reference=data['Reference'],
            owner=user,
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = CustomerSerializer(customer, many=False)
    return Response(serializer.data)


# 고객 수정
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putCustomer(request, pk):
    user = request.user
    customer = Customer.objects.get(id=pk)
    data = request.data
    if customer.owner == user:
        customer.name = data['name']
        customer.address = data['address']
        customer.email = data['email']
        customer.phoneNumber = data['phoneNumber']
        customer.secondPhoneNumber = data['secondPhoneNumber']
        customer.reference = data['Reference']
        customer.save()
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)
    else:
        return Response("수정 실패")


# 고객 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteCustomer(request, pk):
    user = request.user
    customer = Customer.objects.get(id=pk)
    if customer.owner == user:
        customer.delete()
    else:
        return Response('삭제 실패')
    return Response('삭제 성공')
