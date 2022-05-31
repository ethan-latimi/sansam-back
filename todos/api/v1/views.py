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
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTodoList(request):
    user = request.user
    todos = Todo.objects.filter(owner=user)
    page = request.query_params.get('page')
    paginator = Paginator(Todo, 10)
    todos = pagination(page, paginator)
    serializer = TodoSerializer(todos, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 투두 한개 보기
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTodo(request, pk):
    user = request.user
    todos = Todo.objects.get(id=pk)
    if todos.owner == user:
        serializer = TodoSerializer(todos, many=False)
        return Response({'result': serializer.data})
    else:
        return Response('유저 정보가 일치 하지 않습니다.')


# 투두 생성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postTodo(request):
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
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putTodo(request, pk):
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
        return Response("수정 실패")


# 투두 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTodo(request, pk):
    user = request.user
    todo = Todo.objects.get(id=pk)
    if todo.owner == user:
        todo.delete()
    else:
        return Response('삭제 실패')
    return Response('삭제 성공')
