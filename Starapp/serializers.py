from dataclasses import field
from rest_framework import serializers
# Подключаем модель user
from rest_framework.serializers import ModelSerializer
from .models import (User, Post, Like, Unlike)

class UserRegistrSerializer(serializers.ModelSerializer):
    # Поле для повторения пароля
    password2 = serializers.CharField()
    
    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['email', 'username', 'password', 'password2']
 
    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'], # Назначаем Email
            username=self.validated_data['username'], # Назначаем Логин
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя 
        return user

# class PostSerializers(ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['author', 'image','like']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'user', 'post', 'date'
        )
        read_only_fields = ('post', 'user', 'date',)


class UnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unlike
        fields = (
            'user', 'post', 'date'
        )
        read_only_fields = ('post', 'user', 'date',)


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(read_only=True, many=True)
    unlikes = LikeSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = (
            'id', 'author', 'image', 'likes_amount', 'unlikes_amount', 'likes', 'unlikes'
        )