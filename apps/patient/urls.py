from django.conf.urls import url
from django.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', viewset=views.UserViewSet)
router.register('permissions', viewset=views.PermissionViewSet)
router.register('employees', viewset=views.EmployeeViewSet)

urlpatterns = [
    url('auth/login', obtain_jwt_token),
    path('auth/send-code', views.send_code),
    path('', include(router.urls)),
    url('profile', views.profile),
]
