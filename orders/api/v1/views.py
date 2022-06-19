import re
from django.dispatch import receiver
# Django
from rest_framework import status
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from orders.models import Order, OrderItem, OrderImage
from orders.serializers import OrderSerializer, OrderItemSerializer
from core.views import pagination


# 주문 리스트 : 고객별(pk), 연도별, 완료별(isPaid&&isDelivered), 가격별(높음,낮음)
# page, receiver, byPrice, delivered, start, end 쿼리 구성요소
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderList(request):
    regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    user = request.user
    page = request.query_params.get('page')
    receiver = request.query_params.get('receiver')
    isPaid = request.query_params.get('paid')
    byPrice = request.query_params.get('byPrice')
    isDelivered = request.query_params.get("delivered")
    start = request.query_params.get('start')
    end = request.query_params.get('end')
    givenOrder = "-created"
    if byPrice == "true":
        givenOrder = "-price"
    if start != None and end != None:
        start = regex.match(start)
        end = regex.match(end)
    if page == None:
        page = 1
    if start == None or end == None:
        d = timezone.now()
        start = f"{d.year}-{d.month-1}-{d.day}"
        end = f"{d.year}-{d.month}-{d.day+1}"
    else:
        start = start.group()
        end = end.group()
        list = end.split('-')
        end = f"{list[0]}-{list[1]}-{int(list[2])+1}"
    if isPaid:
        if isPaid.lower() == "true":
            isPaid = True
        else:
            isPaid = False
        if receiver:
            orders = Order.objects.filter(owner=user, receiver__icontains=receiver, isPaid=isPaid, created__range=[
                                          start, end]).order_by(givenOrder)
        else:
            orders = Order.objects.filter(owner=user, isPaid=isPaid, created__range=[
                                          start, end]).order_by(givenOrder)
        paginator = Paginator(orders, 10)
        orders = pagination(page, paginator)
        serializer = OrderSerializer(orders, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
    elif isDelivered:
        if isDelivered.lower() == "true":
            isDelivered = True
        else:
            isDelivered = False
        if receiver:
            orders = Order.objects.filter(owner=user, receiver__icontains=receiver, isDelivered=isDelivered, created__range=[
                                          start, end]).order_by(givenOrder)
        else:
            orders = Order.objects.filter(owner=user, isDelivered=isDelivered, created__range=[
                                          start, end]).order_by(givenOrder)
        paginator = Paginator(orders, 10)
        orders = pagination(page, paginator)
        serializer = OrderSerializer(orders, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
    elif isPaid == "true" and isDelivered == "true":
        if isPaid.lower() == "true" and isDelivered.lower() == "true":
            isPaid = True
            isDelivered = True
        else:
            isPaid = False
            isDelivered = False
        if receiver:
            orders = Order.objects.filter(owner=user, receiver__icontains=receiver, isDelivered=isDelivered, isPaid=isPaid, created__range=[
                                          start, end]).order_by(givenOrder)
        else:
            orders = Order.objects.filter(owner=user, isDelivered=isDelivered, isPaid=isPaid, created__range=[
                                          start, end]).order_by(givenOrder)
        paginator = Paginator(orders, 10)
        orders = pagination(page, paginator)
        serializer = OrderSerializer(orders, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
    else:
        orders = Order.objects.filter(owner=user, created__range=[
            start, end]).order_by(givenOrder)
        if receiver:
            orders = Order.objects.filter(owner=user, receiver__icontains=receiver, created__range=[
                start, end]).order_by(givenOrder)
        paginator = Paginator(orders, 10)
        count = orders.count()
        orders = pagination(page, paginator)
        serializer = OrderSerializer(orders, many=True)
        return Response({'result': serializer.data, 'count': count, 'page': page, 'pages': paginator.num_pages})


# 주문 한개 보기: 주문의 이미지와 배송지 정보 같이 보내주기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrder(request, pk):
    user = request.user
    order = Order.objects.get(id=pk)
    if order.owner == user:
        serializer = OrderSerializer(Order, many=False)
        return Response({'result': serializer.data})
    else:
        return Response("주문 한개 보기 실패")


# 한개의 주문과 관련된 주문 아이템 리스트
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def postOrder(request):
    user = request.user
    data = request.data
    try:
        order = Order.objects.create(
            customer=data['customer'],
            payment=data['payment'],
            receiver=data['receiver'],
            owner=user,
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)
    # 주문 한개 만들기: 주문 id 반환

    # 주문 아이템 만들기: 리스트 반환

    # 주문 수정하기:

    # 주문 삭제하기:

    # 주문 아이템 수정하기:

    # 주문 아이템 삭제하기
