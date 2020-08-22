import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


from charity.models import Donation, Institution, Category
from charity.serializers import CategorySerializer, UserSerializer, InstitutionSerializer
from django.contrib.auth.models import User
factory = APIRequestFactory()
request = factory.get('/')
serializer_context = {
    'request': Request(request),
}
# # initialize the APIClient app
# client = Client()

class UserViewSetTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                             email='user@email.com',
                                             password='Top_secret@1')
        self.client = APIClient()


    def test_User_view_set_status_code_if_authenticated(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('user-list'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context=serializer_context)
        # self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_User_view_set_status_code_if_not_authenticated(self):
        response = self.client.get(reverse('user-list'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context=serializer_context)
        # self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_User_view_set_status_code_if_authenticated_check_response(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('user-list'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
