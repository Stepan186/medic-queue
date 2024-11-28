from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = 'apps.users'
    label = 'users'


default_app_config = 'apps.users.UsersAppConfig'
