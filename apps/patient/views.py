import re
from random import randrange

import requests
from django.conf import settings as config
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import User
from .permissions import IsEmployee
from .serializers import UserSerializer, PermissionSerializer
from ..common.mixins import EagerLoadingMixin
from ..common.throttling import SmsRateThrottle


@api_view(['POST'])
@throttle_classes([SmsRateThrottle])
def send_code(request):
    if not re.match(r'^((7)+([0-9]){10})$', request.data.get('phone', '')):
        raise serializers.ValidationError({"phone": "Некорректный формат номера."})

    try:
        user = User.objects.get(phone=request.data['phone'])
    except ObjectDoesNotExist:
        user = User.objects.create(phone=request.data['phone'])
    password = str(randrange(100000, 999999))
    user.password = make_password(password)
    user.save()

    url = 'https://sms.ru/sms/send'
    params = {
        'api_id': config.SMS_RU_TOKEN,
        'to': user.phone,
        'msg': f'Код для авторизации на сайте Дяди Дёнера: {password}.'
    }
    r = requests.get(url=url, params=params)
    # ?api_id=62128A62-4801-1F93-F086-4DDE4F7226F7&to=$order->phone_number&msg=$msg&json=1

    return Response(1)


class EmployeeViewSet(EagerLoadingMixin, ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_employee=True).exclude(is_superuser=True)


class UserViewSet(EagerLoadingMixin, ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.exclude(is_superuser=True)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['last_name', 'first_name', 'phone', 'email']

    def get_permissions(self):
        return [IsAuthenticated(), IsEmployee()]


class PermissionViewSet(ListModelMixin, GenericViewSet):
    queryset = Permission.objects.exclude(content_type__app_label__in=['auth', 'contenttypes', 'sessions', 'silk'])
    serializer_class = PermissionSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    user_dict = UserSerializer(user, context={'request': request}).data
    if user_dict['is_employee']:
        user_dict['permissions'] = user.get_user_permissions()
    return {
        'token': token,
        'user': user_dict
    }


@api_view(['PUT', 'GET', 'DELETE'])
def profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.to_representation(instance=request.user))
    elif request.method == 'PUT':
        serializer = UserSerializer(instance=request.user, data=request.data)
        serializer.is_valid(True)
        instance = serializer.update(instance=request.user, validated_data=serializer.validated_data)
        return Response(serializer.to_representation(instance=instance))
    elif request.method == 'DELETE':
        request.user.delete()
        return Response(1)
