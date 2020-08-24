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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_User_view_set_status_code_if_authenticated_check_response(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('user-list'), format='json')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context=serializer_context)
        self.assertEqual(json.loads(response.content)['results'][0], serializer.data[0])

class GetSingleUserTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(first_name='user1', last_name='user_1', username='test_username1',
                                             email='user1@email.com',
                                             password='1Top_secret@1')
        self.user2 = User.objects.create_user(first_name='user2', last_name='user_2', username='test_username2',
                                             email='user2@email.com',
                                             password='2Top_secret@1')
        self.client = APIClient()

    def test_view_single_user_status_code_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.get(reverse('user-detail', args =[self.user2.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_single_user_status_code_if_not_authenticated(self):
        response = self.client.get(reverse('user-detail', args =[self.user2.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_single_user_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.get(reverse('user-detail', args =[self.user2.pk]), format='json')
        user2 = User.objects.get(pk=self.user2.pk)
        serializer = UserSerializer(user2, context={'request': request})
        self.assertEqual(response.data, serializer.data)

    def test_get_not_valid_single_user_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.get(reverse('user-detail', args =[14]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)