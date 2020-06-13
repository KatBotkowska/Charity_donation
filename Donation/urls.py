"""Donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, reverse_lazy
import django.contrib.auth.views as auth_views
from rest_framework import routers

from charity.APIviews import UserViewSet, CategoryViewSet, InstitutionViewSet, DonationViewSet
from charity.views import MyPasswordResetView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'donations', DonationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('gestion/', admin.site.urls),
    path('password_reset/', MyPasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                                        email_template_name='registration/password_reset_email.html',
                                                        success_url=reverse_lazy('password_reset_done')),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('charity.urls')),
]
