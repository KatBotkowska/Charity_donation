import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from charity.models import Donation, Institution, Category
from charity.serializers import CategorySerializer, UserSerializer, InstitutionSerializer
from django.contrib.auth.models import User
factory = APIRequestFactory()
request = factory.get('/')
serializer_context = {
    'request': Request(request),
}
# initialize the APIClient app
client = Client()

class UserViewSetTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                             email='user@email.com',
                                             password='Top_secret@1')

    def test_User_view_set(self):
        response = client.get(reverse('user-list'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
