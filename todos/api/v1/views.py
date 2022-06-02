from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Django
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from todos.models import Todo
from todos.serializers import TodoSerializer
from core.views import pagination


# 투두 전체보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', TodoSerializer(many=True))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTodoList(request):
    '''
    투두 목록 보기
    ---
    '''
    user = request.user
    todos = Todo.objects.filter(owner=user)
    page = request.query_params.get('page')
    paginator = Paginator(Todo, 10)
    todos = pagination(page, paginator)
    serializer = TodoSerializer(todos, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 투두 한개 보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', TodoSerializer(many=False))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTodo(request, pk):
    '''
    투두 개별 보기
    ---
    '''
    user = request.user
    todos = Todo.objects.get(id=pk)
    if todos.owner == user:
        serializer = TodoSerializer(todos, many=False)
        return Response({'result': serializer.data})
    else:
        message = {'detail': '유저정보가 일치하지 않습니다'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 투두 생성
@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'content'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="제목"),
            'content': openapi.Schema(type=openapi.TYPE_INTEGER, description="내용"),
        },
    ),
    responses={
        201: openapi.Response('successfully created', TodoSerializer),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postTodo(request):
    '''
    투두 생성하기
    ---
    '''
    user = request.user
    data = request.data
    try:
        todo = Todo.objects.create(
            title=data["title"],
            content=data["content"],
            owner=user,
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = TodoSerializer(todo, many=False)
    return Response(serializer.data)


# 투두 수정
@swagger_auto_schema(
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="투두의 pk입니다."),
        ],
        required=['title', 'content'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="제목"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="내용"),
        },
    ),
    responses={
        200: openapi.Response('successfully created', TodoSerializer),
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putTodo(request, pk):
    '''
    투두 수정하기
    ---
    '''
    user = request.user
    todo = Todo.objects.get(id=pk)
    data = request.data
    if todo.owner == user:
        todo.title = data["title"]
        todo.content = data["content"]
        todo.save()
        serializer = TodoSerializer(todo, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '수정 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 투두 삭제
@swagger_auto_schema(
    methods=['delete'],
    responses={
        200: openapi.Response('successfully deleted')
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTodo(request, pk):
    '''
    투두 삭제하기
    ---
    '''
    user = request.user
    todo = Todo.objects.get(id=pk)
    if todo.owner == user:
        todo.delete()
    else:
        message = {'detail': '삭제 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response('삭제 성공')
