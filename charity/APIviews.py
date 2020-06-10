from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Category, Institution, Donation
from .serializers import UserSerializer, CategorySerializer, InstitutionSerializer, DonationSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''API endpoint for users to be viewed or edited'''
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    '''API endpoint for categories to be viewed or edited'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    '''API endpoint for institutions to be viewed or edited'''
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class DonationViewSet(viewsets.ModelViewSet):
    '''API endpoint for donations to be viewed or edited'''
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
