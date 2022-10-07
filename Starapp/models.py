from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class MyUserManager(BaseUserManager):
    # Создаём метод для создания пользователя
    def _create_user(self, email, username, password, **extra_fields):
        # Проверяем есть ли Email
        if not email: 
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Email")
        # Проверяем есть ли логин
        if not username:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Логин")
        # Делаем пользователя
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user
    
    # Делаем метод для создание обычного пользователя
    def create_user(self, email, username, password):
        # Возвращаем нового созданного пользователя
        return self._create_user(email, username, password)
 
    # Делаем метод для создание админа сайта
    def create_superuser(self, email, username, password):
        # Возвращаем нового созданного админа
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)

# Создаём класс User
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True) # Идентификатор
    username = models.CharField(max_length=50, unique=True) # Логин
    email = models.EmailField(max_length=100, unique=True) # Email
    is_active = models.BooleanField(default=True) # Статус активации
    is_staff = models.BooleanField(default=False) # Статус админа
    
    USERNAME_FIELD = 'email' # Идентификатор для обращения 
    REQUIRED_FIELDS = ['username'] # Список имён полей для Superuser
 
    objects = MyUserManager() # Добавляем методы класса MyUserManager
    
    # Метод для отображения в админ панели
    def __str__(self):
        return self.email

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='IM/%Y/%m')
    # like = models.PositiveIntegerField(default=0)
    
    
    @property
    def likes_amount(self):
        return self.likes.all().count()

    def unlikes_amount(self):
        return self.unlikes.all().count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.post.name


class Unlike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='unlikes')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.post.name
   
# Create your models here.
