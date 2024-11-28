from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core import validators
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=False, unique=True,
                             error_messages={'unique': "Пользователь с таким телефоном уже зарегистрирован."})
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = ('first_name', 'phone', 'last_name')

   class Meta:
        db_table = 'users'
        permissions = (
            ('view', 'Просмотр списка пользователей'),
            ('update', 'Редактирование пользователей'),
            ('assign_employee', 'Назначение сотрудников'),
        )
        default_permissions = ()

    objects = BaseUserManager()
