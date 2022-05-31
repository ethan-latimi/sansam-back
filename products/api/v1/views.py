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
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProductList(request):
    user = request.user
    products = Product.objects.filter(owner=user)
    page = request.query_params.get('page')
    paginator = Paginator(products, 10)
    products = pagination(page, paginator)
    serializer = ProductSerializer(products, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 상품 한개 보기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProduct(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    if product.owner == user:
        serializer = ProductSerializer(product, many=False)
        return Response({'result': serializer.data})
    else:
        return Response('유저 정보가 일치 하지 않습니다.')


# 상품 생성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postProduct(request):
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
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putProduct(request, pk):
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
        return Response("수정 실패")


# 상품 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteProduct(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    if product.owner == user:
        product.delete()
    else:
        return Response('삭제 실패')
    return Response('삭제 성공')


# 카테고리 전체 보기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCategoryList(request):
    user = request.user
    category = Category.objects.filter(owner=user)
    page = request.query_params.get('page')
    paginator = Paginator(category, 10)
    category = pagination(page, paginator)
    serializer = CategorySerializer(category, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 카테고리 생성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postCategory(request):
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
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putCategory(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    data = request.data
    if category.owner == user:
        category.name = data["name"]
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)
    else:
        return Response("수정 실패")


# 카테고리 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteCategory(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.owner == user:
        category.delete()
    else:
        return Response('삭제 실패')
    return Response('삭제 성공')
