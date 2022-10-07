from django.shortcuts import render
from rest_framework import status
# Подключаем компонент для ответа
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny, BasePermissionMetaclass, IsAdminUser
# Подключаем модель User
from .models import User, Post
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, PostSerializer, Like, LikeSerializer, Unlike, UnlikeSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
# декоратор action
from rest_framework.decorators import action

 
 
# Создаём класс RegistrUserView
class RegistrUserView(CreateAPIView):
    # Добавляем в queryset
    queryset = User.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]
    
    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else: # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)


# class PostView(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAdminUser]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['get', ], detail=True, serializer_class=LikeSerializer)
    def likes(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        unlike = Unlike.objects.filter(user=user, post=post)
        like = Like.objects.filter(user=user, post=post)
        if like.exists():
            like.delete()
            return Response({"message": 'deleted'})
        elif unlike.exists():
            unlike.delete()
            Like.objects.create(user=user, post=post)
            return Response({"message": 'deleted'})
        Like.objects.create(user=user, post=post)
        return Response({"message": 'created'})

    @action(methods=['get', ], detail=True, serializer_class=UnlikeSerializer)
    def unlikes(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        unlike = Unlike.objects.filter(user=user, post=post)
        like = Like.objects.filter(user=user, post=post)
        if unlike.exists():
            unlike.delete()
            return Response({"message": 'deleted'})
        elif like.exists():
            like.delete()
            Unlike.objects.create(user=user, post=post)
            return Response({"message": 'deleted'})
        Unlike.objects.create(user=user, post=post)
        return Response({"message": 'created'})
# Create your views here.
