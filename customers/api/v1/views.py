from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Django
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.views import pagination

# Project
from customers.models import Customer
from customers.serializers import CustomerSerializer, MemoSerializer
from orders.models import Order


@swagger_auto_schema(
    methods=['get'],
    manual_parameters=[
        openapi.Parameter("keyword", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="고객의 이름을 검색합니다"),
        openapi.Parameter("page", openapi.IN_QUERY,
                          type=openapi.TYPE_STRING, description="페이지"),
        openapi.Parameter("order", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="매출에 따른 고객 정렬(false=낮은, true=높은)"),
    ],
    responses={200: openapi.Response(
        'successfully patched', CustomerSerializer(many=True))},
)
# 고객 전체 보기
# (고객 정보를 이용하여 검색): 이름, 매출정렬(false=낮은, true=높은)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCustomerList(request):
    '''
    고객 전체보기
    ---
    고객 리스트 입니다.
    '''
    user = request.user
    query = request.query_params.get('keyword')
    order = request.query_params.get('order')
    if order == None:
        order = 'true'
    if query == None:
        query = ''
    if order.lower() == 'false':
        customers = Customer.objects.filter(
            owner=user, name__icontains=query).order_by('totalSpend')
    elif order.lower() == 'true':
        customers = Customer.objects.filter(
            owner=user, name__icontains=query).order_by('-totalSpend')
    count = customers.count()
    serializer = CustomerSerializer(customers, many=True)
    return Response({'result': serializer.data, 'count': count})


# 고객 한명 보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', CustomerSerializer(many=False))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCustomer(request, pk):
    '''
    고객 한명 보기
    ---
    pk를 통한 고객 한명의 정보를 구해올 수 있습니다.
    '''
    user = request.user
    customer = Customer.objects.get(id=pk)
    if user == customer.owner:
        serializer = CustomerSerializer(customer, many=False)
        return Response({'result': serializer.data})
    else:
        message = {'detail': "해당하는 고객이 없습니다."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 고객 입력 (고객 전체보기를 통해 고객의 아이디를 reference에 넣어줍니다.)
@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'address', 'email', 'phoneNumber'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="고객 이름"),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description="고객 주소"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="고객 이메일"),
            'phoneNumber': openapi.Schema(type=openapi.TYPE_STRING, description="고객 핸드폰 번호(regex유)"),
            'secondPhoneNumber': openapi.Schema(type=openapi.TYPE_STRING, description="고객 서브폰 번호"),
            'reference': openapi.Schema(type=openapi.TYPE_STRING, description="소개자"),
        },
    ),
    responses={
        201: openapi.Response('successfully created', CustomerSerializer),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postCustomer(request):
    '''
    고객 입력
    ---
    고객 전체보기를 통해 고객의 소개자를 찾을 수 있는 란이 있고 이를 통해 소개자란에 string으로 이름을 넣을 수 있으면 합니다.
    '''
    user = request.user
    data = request.data
    try:
        customer = Customer.objects.create(
            name=data['name'],
            address=data['address'],
            email=data['email'],
            phoneNumber=data['phoneNumber'],
            secondPhoneNumber=data['secondPhoneNumber'],
            reference=data['reference'],
            owner=user,
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었거나 중복입니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = CustomerSerializer(customer, many=False)
    return Response(serializer.data)


# 고객 수정
@swagger_auto_schema(
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="고객의 pk입니다."),
        ],
        required=['name', 'address', 'email', 'phoneNumber'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="고객 이름"),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description="고객 주소"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="고객 이메일"),
            'phoneNumber': openapi.Schema(type=openapi.TYPE_STRING, description="고객 핸드폰 번호(regex유)"),
            'secondPhoneNumber': openapi.Schema(type=openapi.TYPE_STRING, description="고객 서브폰 번호"),
            'reference': openapi.Schema(type=openapi.TYPE_STRING, description="소개자"),
        },
    ),
    responses={
        200: openapi.Response('successfully created', CustomerSerializer),
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putCustomer(request, pk):
    '''
    고객 정보 수정
    ---
    고객의 정보를 수정 할 수 있습니다.
    단) 각각의 필드에 기존의 정보를 가져와서 form에 넣어주시고 다시 보내 주어야 합니다.
    '''
    user = request.user
    customer = Customer.objects.get(id=pk)
    data = request.data
    if customer.owner == user:
        customer.name = data['name']
        customer.address = data['address']
        customer.email = data['email']
        customer.company = data['company']
        customer.phoneNumber = data['phoneNumber']
        customer.secondPhoneNumber = data['secondPhoneNumber']
        customer.reference = data['reference']
        customer.save()
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '수정 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 고객 삭제
@swagger_auto_schema(
    methods=['delete'],
    responses={
        200: openapi.Response('successfully deleted')
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteCustomer(request, pk):
    '''
    고객의 id를 가져와 삭제합니다.
    '''
    user = request.user
    customer = Customer.objects.get(id=pk)
    if customer.owner == user:
        customer.delete()
    else:
        message = {'detail': '삭제 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response('삭제 성공')


# 고객 관련 메모
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMemos(request, pk):
    user = request.user
    customer = Customer.objects.get(id=pk)
    if customer.owner == user:
        orders = Order.objects.filter(customer=customer)
        serializer = MemoSerializer(orders, many=True)
        return Response(serializer.data)
    else:
        pass
