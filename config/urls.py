"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve

urlpatterns = [
    path('api/auth/', include('rest_framework.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.attributes.urls')),
    path('api/', include('apps.categories.urls')),
    path('api/', include('apps.uploads.urls')),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.feedback.urls')),
    path('api/', include('apps.reviews.urls')),
    path('api/', include('apps.supplements.urls')),
    path('api/', include('apps.ingredients.urls')),
    path('api/', include('apps.orders.urls')),
    path('api/', include('apps.pick_points.urls')),
    path('api/', include('apps.settings.urls')),
    path('api/', include('apps.promos.urls')),
    path('', include('apps.sberbank.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk')),
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
