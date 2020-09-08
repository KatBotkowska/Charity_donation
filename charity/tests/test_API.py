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

class CreateNewUserTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(first_name='user1', last_name='user_1', username='test_username1',
                                             email='user1@email.com',
                                             password='1Top_secret@1')
        self.valid_payload = {'imie':'user2', 'nazwisko':'user_2',
                                             'email':'user2@email.com',
                                             'haslo':'2Top_secret@1'}
        self.invalid_payload = {'imie':'user2', 'nazwisko':'user_2',
                                             'email':'user2email.com',
                                             'haslo':'aa'}
        self.client = APIClient()

    def test_create_valid_user(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.post(reverse('user-list'), data = json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_not_valid_user(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.post(reverse('user-list'), data = json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_if_not_authenticated(self):
        response = self.client.post(reverse('user-list'), data = json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UpdateUserPutTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(first_name='user1', last_name='user_1', username='test_username1',
                                             email='user1@email.com',
                                             password='1Top_secret@1')
        self.user2 = User.objects.create_user(first_name='user2', last_name='user_2', username='test_username2',
                                             email='user2@email.com',
                                             password='2Top_secret@1')
        self.valid_payload = {'imie':'user2_update', 'nazwisko':'user_2_update',
                                             'email':'user2@email.com',
                                             'haslo':'2Top_secret@1'}
        self.invalid_payload = {'imie':'user2', 'nazwisko':'user_2',
                                             'email':'user2email.com',
                                             'haslo':'aa'}
        self.client = APIClient()

    def test_update_user_status_code_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.put(reverse('user-detail', args =[self.user2.pk]), data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_status_code_if_not_authenticated(self):
        response = self.client.put(reverse('user-detail', args =[self.user2.pk]), data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_status_code_if_authenticated_not_valid_data(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.put(reverse('user-detail', args =[self.user2.pk]), data = json.dumps(self.invalid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateUserPatchTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(first_name='user1', last_name='user_1', username='test_username1',
                                             email='user1@email.com',
                                             password='1Top_secret@1')
        self.user2 = User.objects.create_user(first_name='user2', last_name='user_2', username='test_username2',
                                             email='user2@email.com',
                                             password='2Top_secret@1')
        self.valid_payload = {'imie':'user2_update', 'nazwisko':'user_2_update',
                                             'email':'user2@email.com',
                                             'haslo':'2Top_secret@1'}
        self.invalid_payload = {'imie':'user2', 'nazwisko':'user_2',
                                             'email':'user2email.com',
                                             'haslo':'aa'}
        self.client = APIClient()

    def test_update_user_status_code_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.patch(reverse('user-detail', args =[self.user2.pk]), data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_status_code_if_not_authenticated(self):
        response = self.client.patch(reverse('user-detail', args =[self.user2.pk]), data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_status_code_if_authenticated_not_valid_data(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.patch(reverse('user-detail', args =[self.user2.pk]), data = json.dumps(self.invalid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteUserTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(first_name='user1', last_name='user_1', username='test_username1',
                                             email='user1@email.com',
                                             password='1Top_secret@1')
        self.user2 = User.objects.create_user(first_name='user2', last_name='user_2', username='test_username2',
                                              email='user2@email.com',
                                              password='2Top_secret@1')
        self.client = APIClient()

    def test_delete_valid_user(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.delete(reverse('user-detail', args=[self.user2.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse('user-detail', args=[self.user2.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_valid_user(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.delete(reverse('user-detail', args=[10]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_if_not_authenticated(self):
        response = self.client.delete(reverse('user-detail', args=[self.user2.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                             email='user@email.com',
                                             password='Top_secret@1')
        self.test_category_zabawki = Category.objects.create(name='zabawki')
        self.test_category_meble = Category.objects.create(name='meble')
        self.test_category_ubrania = Category.objects.create(name='ubrania')
        self.client = APIClient()


    def test_category_view_set_status_code_if_authenticated(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('category-list'))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context=serializer_context)
        # self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_view_set_status_code_if_not_authenticated(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_view_set_status_code_if_authenticated_check_response(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('category-list'), format='json')
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context=serializer_context)
        self.assertEqual(json.loads(response.content)['results'][0], serializer.data[0])

class GetSingleCategoryTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                             email='user@email.com',
                                             password='Top_secret@1')
        self.test_category_zabawki = Category.objects.create(name='zabawki')
        self.test_category_meble = Category.objects.create(name='meble')
        self.test_category_ubrania = Category.objects.create(name='ubrania')
        self.client = APIClient()

    def test_view_single_category_status_code_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.get(reverse('category-detail', args =[self.test_category_zabawki.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_single_category_status_code_if_not_authenticated(self):
        response = self.client.get(reverse('category-detail', args =[self.test_category_zabawki.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_single_category_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.get(reverse('category-detail', args =[self.test_category_zabawki.pk]), format='json')
        category_zabawki = Category.objects.get(pk=self.test_category_zabawki.pk)
        serializer = CategorySerializer(category_zabawki, context={'request': request})
        self.assertEqual(response.data, serializer.data)

    def test_get_not_valid_single_category_if_authenticated(self):
        self.client.login(username='test_username1', password='1Top_secret@1')
        response = self.client.get(reverse('category-detail', args =[23]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateCategoryPutTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                                  email='user@email.com',
                                                  password='Top_secret@1')
        self.test_category_zabawki = Category.objects.create(name='zabawki')
        self.test_category_meble = Category.objects.create(name='meble')
        self.test_category_ubrania = Category.objects.create(name='ubrania')

        self.valid_payload = {'name':'nowe zabawki'}
        self.invalid_payload = {'name':''}
        self.client = APIClient()

    def test_update_category_status_code_if_authenticated(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.put(reverse('category-detail', args =[self.test_category_zabawki.pk]),
                                   data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_status_code_if_not_authenticated(self):
        response = self.client.put(reverse('category-detail', args =[self.test_category_zabawki.pk]),
                                   data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_category_status_code_if_authenticated_not_valid_data(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.put(reverse('category-detail', args =[self.test_category_zabawki.pk]),
                                   data = json.dumps(self.invalid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateCategoryPatchTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                                  email='user@email.com',
                                                  password='Top_secret@1')
        self.test_category_zabawki = Category.objects.create(name='zabawki')
        self.test_category_meble = Category.objects.create(name='meble')
        self.test_category_ubrania = Category.objects.create(name='ubrania')

        self.valid_payload = {'name':'nowe zabawki'}
        self.invalid_payload = {'name':''}
        self.client = APIClient()

    def test_update_category_status_code_if_authenticated(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.patch(reverse('category-detail', args =[self.test_category_zabawki.pk]),
                                   data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_status_code_if_not_authenticated(self):
        response = self.client.patch(reverse('category-detail', args =[self.test_category_zabawki.pk]),
                                   data = json.dumps(self.valid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_category_status_code_if_authenticated_not_valid_data(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.patch(reverse('category-detail', args =[self.test_category_zabawki.pk]),
                                   data = json.dumps(self.invalid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteCategoryTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                                  email='user@email.com',
                                                  password='Top_secret@1')
        self.test_category_zabawki = Category.objects.create(name='zabawki')
        self.test_category_meble = Category.objects.create(name='meble')
        self.test_category_ubrania = Category.objects.create(name='ubrania')
        self.client = APIClient()

    def test_delete_valid_category(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.delete(reverse('category-detail', args=[self.test_category_zabawki.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse('category-detail', args=[self.test_category_zabawki.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_valid_category(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.delete(reverse('category-detail', args=[10]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_if_not_authenticated(self):
        response = self.client.delete(reverse('category-detail', args=[self.test_category_zabawki.pk]), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)