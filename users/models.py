from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    object = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'Kullanici'
        verbose_name_plural = 'Kullanicilar'