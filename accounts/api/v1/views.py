from datetime import timedelta
import re
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Django
from rest_framework import status
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum

# Project
from ...models import Account, Transaction
from accounts.serializers import AccountSerializer, TransactionSerializer
from core.views import pagination
from customers.models import Customer


# 자신의 계좌 보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', AccountSerializer(many=False))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAccount(request):
    '''
    유저의 계좌
    ---
    ### 한유저는 하나의 계좌를 가지고 있게 됩니다.
    '''
    user = request.user
    account = Account.objects.get(owner=user)
    enddate = timezone.now()
    startdate = enddate - timedelta(days=6)
    year = enddate.strftime("%Y")

    month = startdate.strftime("%m")
    deposits = Transaction.objects.filter(
        account=account, type="deposit", updated__month=month).order_by('-created')
    expenses = Transaction.objects.filter(
        account=account, type="expense", updated__month=month).order_by('-created')
    depositsStatus = Transaction.objects.filter(
        account=account, type="deposit", updated__range=[startdate, enddate]).order_by('-created')
    expensesStatus = Transaction.objects.filter(
        account=account, type="expense", updated__range=[startdate, enddate]).order_by('-created')
    walletSerializer = AccountSerializer(account, many=False)
    depositSerializer = TransactionSerializer(deposits, many=True)
    expenseSerializer = TransactionSerializer(expenses, many=True)
    depositStatusSerializer = TransactionSerializer(depositsStatus, many=True)
    expenseStatusSerializer = TransactionSerializer(expensesStatus, many=True)
    deposit = 0
    expense = 0
    depositStatus = 0
    expenseStatus = 0
    monthlySales = []
    yearlySales = 0
    for i in range(12):
        sale = Transaction.objects.filter(
            account=account, created__year=year, type="deposit", updated__month=i+1).aggregate(sum=Sum('amount'))
        if sale["sum"]:
            monthlySales.append(sale["sum"])
            yearlySales += sale["sum"]
        else:
            monthlySales.append(0)
    for i in depositSerializer.data:
        deposit += i["amount"]
    for i in expenseSerializer.data:
        expense += i["amount"]
    for i in depositStatusSerializer.data:
        depositStatus += i["amount"]
    for i in expenseStatusSerializer.data:
        expenseStatus += i["amount"]
    walletStatus = depositStatus - expenseStatus
    queryList = {"wallet": {"title": "잔고", "amount": format(walletSerializer.data["wallet"], ','), "status": walletStatus},
                 "deposit": {"title": "수입", "amount": format(deposit, ','), "status": depositStatus}, "expense": {"title": "지출", "amount": format(expense, ','), "status": expenseStatus}, 'monthlyReport': monthlySales, 'yearlySales': yearlySales/10000}

    return Response(queryList)


@api_view(["GET"])
def getDashboard(request):
    pass

# 모든 거래내역 보기: 입금, 출금, 날짜별


@swagger_auto_schema(
    methods=['get'],
    manual_parameters=[
        openapi.Parameter("sort", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="입/출금분류 deposit(입금)과 expense(출금)으로 나뉩니다"),
        openapi.Parameter("page", openapi.IN_QUERY,
                          type=openapi.TYPE_STRING, description="페이지"),
        openapi.Parameter("start", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="0000-00-00으로 설정해야 하며 날짜별 검색의 시작날짜를 설정합니다"),
        openapi.Parameter("end", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="0000-00-00으로 설정해야 하며 날짜별 검색의 종료날짜를 설정합니다"),
    ],
    responses={200: openapi.Response(
        'successfully patched', TransactionSerializer(many=True))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTransaction(request):
    '''
    거래내역 보기
    ---
    ### 한 계좌의 모든 거래내역을 볼 수 있습니다.
    - 검색: 날짜별, 입금별, 출금별
    - 날짜를 쿼리에 담지 않은 경우 최근 한달의 기간을 자동으로 설정하게 되어 있습니다.
    '''
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
@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['type', 'content', 'amount', 'customer'],
        properties={
            'type': openapi.Schema(type=openapi.TYPE_STRING, description="입/출금을 입력란(deposit/expense)"),
            'amount': openapi.Schema(type=openapi.TYPE_STRING, description="금액 입력란. 없을시 0"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="거래내용 입력란, 빈문자열 가능"),
            'customer': openapi.Schema(type=openapi.TYPE_INTEGER, description="거래 고객의 pk 입력란"),
        },
    ),
    responses={
        201: openapi.Response('successfully created', TransactionSerializer),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postTransaction(request):
    '''
    거래내역 입력하기
    ---
    ### 계좌에 등록되는 거래 내역입니다.
    - 검색: 날짜별, 입금별, 출금별
    - 날짜를 쿼리에 담지 않은 경우 최근 한달의 기간을 자동으로 설정하게 되어 있습니다.
    '''
    account = request.user.account
    data = request.data
    try:
        deposit = Transaction.objects.create(
            amount=data['amount'],
            type=data['type'],
            account=account,
            content=data['content'],
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = TransactionSerializer(deposit, many=False)
    return Response(serializer.data)


# 거래내역 수정
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putTransaction(request, pk):
    account = request.user.account
    transaction = Transaction.objects.get(id=pk)
    data = request.data
    if transaction.account == account:
        transaction.amount = data["amount"]
        transaction.type = data["type"]
        transaction.content = data["content"]

        transaction.save()
        message = {'detail': '수정 성공'}
        return Response(message)
    else:
        message = {'detail': '수정 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# 거래내역 삭제


@swagger_auto_schema(
    methods=['delete'],
    responses={
        200: openapi.Response('successfully deleted')
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTransaction(request, pk):
    '''
    거래 내역 삭제
    ---
    파라미터에 있는 pk를 비교하여 유저의 정보와 일치한다면 삭제합니다.
    - pk는 해당 transaction의 id 입니다.
    '''
    account = request.user.account
    transaction = Transaction.objects.get(id=pk)
    if transaction.account == account:
        transaction.delete()
    else:
        message = {'detail': '삭제 실패(유저 정보 or id가 잘못 되었습니다.)'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response('successfully deleted')
