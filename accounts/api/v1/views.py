import re

# Django
from rest_framework import status
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import Customer


# Project
from ...models import Account, Transaction
from accounts.serializers import AccountSerializer, TransactionSerializer
from core.views import pagination


# 자신의 계좌 보기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAccount(request):
    user = request.user
    account = Account.objects.get(owner=user)
    serializer = AccountSerializer(account, many=False)
    return Response(serializer.data)


# 모든 거래내역 보기(입금, 출금, 날짜별)
# 아무 숫자를 입력할 경우가 있을수 있음 ex) 3000-19-21(오류)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTransaction(request):
    regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    account = request.user.account
    query = request.query_params.get('sort')
    page = request.query_params.get('page')
    start = request.query_params.get('start')
    end = request.query_params.get('end')
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
    if query == 'deposit':
        deposits = Transaction.objects.filter(
            account=account, type=query).order_by('-created')
        paginator = Paginator(deposits, 10)
        deposits = pagination(page, paginator)
        serializer = TransactionSerializer(deposits, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
    elif query == 'expense':
        expenses = Transaction.objects.filter(
            account=account, type=query).order_by('-created')
        paginator = Paginator(expenses, 10)
        expenses = pagination(page, paginator)
        serializer = TransactionSerializer(expenses, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
    else:
        transactions = Transaction.objects.filter(
            account=account, created__range=[start, end]).order_by('-created')
        paginator = Paginator(transactions, 10)
        transactions = pagination(page, paginator)
        serializer = TransactionSerializer(transactions, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 거래내역 입력
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postTransaction(request):
    user = request.user
    account = request.user.account
    data = request.data
    customer = Customer.objects.get(id=data["customer"])
    try:
        deposit = Transaction.objects.create(
            amount=data['amount'],
            type=data['type'],
            account=account,
            content=data['content'],
            customer=customer
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = TransactionSerializer(deposit, many=False)
    return Response(serializer.data)


# 거래내역 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTransaction(request, pk):
    account = request.user.account
    transaction = Transaction.objects.get(id=pk)
    if transaction.account == account:
        transaction.delete()
    else:
        return Response('삭제 실패')
    return Response('성공적으로 삭제 되었습니다.')
