from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core import validators
from django.db import models


class Queue(AbstractBaseUser, PermissionsMixin):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField('active', default=True, )

    def __str__(self):
        return f"{self.position}: {self.patient.name}"
