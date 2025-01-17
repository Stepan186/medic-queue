# Generated by Django 3.1.4 on 2021-01-28 06:57

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(
                    error_messages={'unique': 'Пользователь с такой электронной почтой уже зарегистрирован.'},
                    max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone',
                 models.CharField(error_messages={'unique': 'Пользователь с таким телефоном уже зарегистрирован.'},
                                  max_length=255, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_employee', models.BooleanField(default=False)),
                ('position', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'users',
                'permissions': (('view', 'Просмотр списка пользователей'), ('update', 'Редактирование пользователей'),
                                ('assign_employee', 'Назначение сотрудников')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='FavoritePosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_positions_pivot',
                                   to='products.position')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_positions_pivot',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite_positions',
                'permissions': (),
                'default_permissions': (),
                'unique_together': {('position', 'user')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_positions',
            field=models.ManyToManyField(related_name='liked_users', through='users.FavoritePosition',
                                         to='products.Position'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True,
                                         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                         related_name='user_set', related_query_name='user', to='auth.Group',
                                         verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                         related_name='user_set', related_query_name='user', to='auth.Permission',
                                         verbose_name='user permissions'),
        ),
    ]
