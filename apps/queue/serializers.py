from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from ..common.serializers import BaseModelSerializer


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UserSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    permissions = PermissionSerializer(many=True, source='user_permissions', read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, write_only=True)

    def validate(self, data):
        if not self.instance and 'password' not in data:
            raise ValidationError({'password': 'Password required!'})

        if 'password' in data:
            if data.get('password') != self.initial_data.get('password_confirmation'):
                raise ValidationError({'password_confirmation': 'Пароли не совпадают.'})
            data['password'] = make_password(data.get('password'))

        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        if user.is_employee:
            user.user_permissions.set(permissions, clear=True)

        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.is_employee:
            instance.user_permissions.set(permissions, clear=True)

        return instance

    def to_representation(self, instance):
        user = super().to_representation(instance)
        if not user['is_employee']:
            user.pop('position', None)
            user.pop('permissions', None)

        return user

    class Meta:
        model = User
        extra_kwargs = {
            "first_name": {
                "error_messages": {
                    "required": "Необходимо заполнить поле Имя.",
                    "null": "Необходимо заполнить поле Имя.",
                }
            },
            "phone": {
                "error_messages": {
                    "required": "Необходимо заполнить поле Телефон.",
                    "null": "Необходимо заполнить поле Телефон.",
                    "unique": "Поле Телефон должно быть уникальным.",
                }
            },
        }
