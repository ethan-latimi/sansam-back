from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Django
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from core.views import pagination


# 상품 전체보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', ProductSerializer(many=True))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProductList(request):
    '''
    상품 목록보기
    ----
    '''
    user = request.user
    query = request.query_params.get('keyword')
    if query:
        products = Product.objects.filter(
            owner=user, name__icontains=query).order_by('created')
    else:
        products = Product.objects.filter(
            owner=user).order_by('created')
    serializer = ProductSerializer(products, many=True)
    return Response({'result': serializer.data})


# 상품 한개 보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', ProductSerializer(many=False))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProduct(request, pk):
    '''
    상품 개별 보기
    ---
    '''
    user = request.user
    product = Product.objects.get(id=pk)
    if product.owner == user:
        serializer = ProductSerializer(product, many=False)
        return Response({'result': serializer.data})
    else:
        message = {'detail': '유저 정보가 일치하지 않습니다'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 상품 생성
@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'price', 'qty', 'category'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="상품 이름"),
            'price': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 가격"),
            'qty': openapi.Schema(type=openapi.TYPE_INTEGER, description="상품 수량"),
            'category': openapi.Schema(type=openapi.TYPE_INTEGER, description="해당하는 카테고리의 아이디를 입력"),
        },
    ),
    responses={
        201: openapi.Response('successfully created', ProductSerializer),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postProduct(request):
    '''
    상품 생성하기
    ---
    '''
    user = request.user
    data = request.data
    try:
        category = Category.objects.get(id=data["category"])
        product = Product.objects.create(
            name=data["name"],
            price=data["price"],
            qty=data["qty"],
            category=category,
            owner=user
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# 상품 수정
@swagger_auto_schema(
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="상품의 pk입니다."),
        ],
        required=['name', 'price', 'qty'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="상품 이름"),
            'price': openapi.Schema(type=openapi.TYPE_STRING, description="상품 가격"),
            'qty': openapi.Schema(type=openapi.TYPE_STRING, description="상품 수량"),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description="상품 카테고리"),
        },
    ),
    responses={
        200: openapi.Response('successfully created', ProductSerializer),
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putProduct(request, pk):
    '''
    상품 수정하기
    ---
    '''
    user = request.user
    product = Product.objects.get(id=pk)
    data = request.data

    if product.owner == user:
        product.name = data["name"]
        product.price = data["price"]
        product.qty = data["qty"]
        if data["category"]:
            category = Category.objects.get(id=data["category"])
            product.category = category
        product.save()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '수정 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 상품 삭제
@swagger_auto_schema(
    methods=['delete'],
    responses={
        200: openapi.Response('successfully deleted')
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteProduct(request, pk):
    '''
    상품 삭제하기
    ---
    '''
    user = request.user
    product = Product.objects.get(id=pk)
    if product.owner == user:
        product.delete()
    else:
        message = {'detail': '삭제 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response('삭제 성공')


# 카테고리 전체 보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', CategorySerializer(many=True))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCategoryList(request):
    '''
    카테고리 목록 보기
    ---
    '''
    user = request.user
    category = Category.objects.filter(owner=user)
    page = request.query_params.get('page')
    paginator = Paginator(category, 10)
    category = pagination(page, paginator)
    serializer = CategorySerializer(category, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 카테고리 생성
@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="카테고리 이름"),
        },
    ),
    responses={
        201: openapi.Response('successfully created', ProductSerializer),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postCategory(request):
    '''
    카테고리 생성하기
    ---
    '''
    user = request.user
    data = request.data
    try:
        category = Category.objects.create(
            name=data['name'],
            owner=user,
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)


# 카테고리 수정
@swagger_auto_schema(
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="카테고리의 pk입니다."),
        ],
        required=['name'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="카테고리 이름"),
        },
    ),
    responses={
        200: openapi.Response('successfully created', CategorySerializer),
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putCategory(request, pk):
    '''
    카테고리 수정하기
    ---
    '''
    user = request.user
    category = Category.objects.get(id=pk)
    data = request.data
    if category.owner == user:
        category.name = data["name"]
        category.save()
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '수정 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 카테고리 삭제
@swagger_auto_schema(
    methods=['delete'],
    responses={
        200: openapi.Response('successfully deleted')
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteCategory(request, pk):
    '''
    카테고리 삭제하기
    ---
    '''
    user = request.user
    category = Category.objects.get(id=pk)
    if category.owner == user:
        category.delete()
    else:
        message = {'detail': '삭제 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response('삭제 성공')
