# Django
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from farms.models import Farm, Log
from farms.serializers import FarmSerializer, LogSerializer
from core.views import pagination


# 농장 리스트
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFarmList(request):
    user = request.user
    farms = Farm.objects.filter(owner=user)
    page = request.query_params.get('page')
    paginator = Paginator(farms, 10)
    farms = pagination(page, paginator)
    serializer = FarmSerializer(farms, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 농장 한개 보기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFarm(request, pk):
    user = request.user
    farm = Farm.objects.get(id=pk)
    if farm.owner == user:
        serializer = FarmSerializer(farm, many=False)
        return Response({'result': serializer.data})
    else:
        return Response('유저 정보가 일치 하지 않습니다.')


# 농장 생성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postFarm(request):
    user = request.user
    data = request.data
    try:
        farm = Farm.objects.create(
            title=data['title'],
            introduction=data['introduction'],
            description=data['description'],
            owner=user,
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = FarmSerializer(farm, many=False)
    return Response(serializer.data)


# 농장 수정
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putFarm(request, pk):
    user = request.user
    farm = Farm.objects.get(id=pk)
    data = request.data
    if farm.owner == user:
        farm.title = data["title"]
        farm.introduction = data["introduction"]
        farm.description = data["description"]
        farm.save()
        serializer = FarmSerializer(farm, many=False)
        return Response(serializer.data)
    else:
        return Response("수정 실패")


# 농장 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteFarm(request, pk):
    user = request.user
    farm = Farm.objects.get(id=pk)
    if farm.owner == user:
        farm.delete()
    else:
        return Response('삭제 실패')
    return Response('삭제 성공')


# 일지 리스트
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getLogList(request, farm_pk):
    user = request.user
    try:
        farm = Farm.objects.get(id=farm_pk)
    except:
        return Response('farm does not exists')
    if user == farm.owner:
        logs = Log.objects.filter(farm_id=farm_pk)
        page = request.query_params.get('page')
        paginator = Paginator(logs, 10)
        logs = pagination(page, paginator)
        serializer = LogSerializer(logs, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
    else:
        return Response('일지 찾기 실패')

# 일지 한개 보기


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getLog(request, log_pk):
    user = request.user
    log = Log.objects.filter(owner=user, id=log_pk)
    serializer = LogSerializer(log, many=True)
    return Response({'result': serializer.data})


# 일지 생성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postLog(request, farm_pk):
    data = request.data
    farm = Farm.objects.get(id=farm_pk)
    try:
        log = Log.objects.create(
            title=data['title'],
            content=data['content'],
            farm=farm
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = LogSerializer(log, many=False)
    return Response(serializer.data)


# 일지 수정
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putLog(request, log_pk):
    user = request.user
    log = Log.objects.get(id=log_pk)
    farm = log.farm
    data = request.data
    if farm.owner == user:
        log.title = data['title']
        log.content = data["content"]
        log.save()
        serializer = LogSerializer(log, many=False)
        return Response(serializer.data)
    else:
        return Response("수정 실패")


# 일지 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteLog(request, log_pk):
    user = request.user
    log = Log.objects.get(id=log_pk)
    owner = log.farm.owner
    if owner == user:
        log.delete()
    else:
        return Response('삭제 실패')
    return Response('삭제 성공')
