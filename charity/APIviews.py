from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions
from .models import Category, Institution, Donation
from .serializers import UserSerializer, CategorySerializer, InstitutionSerializer, DonationSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for users to be viewed or edited"""
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]
    permission_classes = [permissions.IsAuthenticated]  # override default list in settings


class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for categories to be viewed or edited"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', ]


class InstitutionViewSet(viewsets.ModelViewSet):
    """API endpoint for institutions to be viewed or edited"""
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', ]


class DonationViewSet(viewsets.ModelViewSet):
    """API endpoint for donations to be viewed or edited"""
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['institution', ]
