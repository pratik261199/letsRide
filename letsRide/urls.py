"""letsRide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet, RiderViewSet, RequesterViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"rider", RiderViewSet, basename="rider")
router.register(r"requester", RequesterViewSet, basename="requester")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
]
