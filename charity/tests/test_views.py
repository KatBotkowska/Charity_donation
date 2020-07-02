from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from charity.models import Category, Institution, Donation

class LandingPageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category_1 = Category.objects.create(name='test_category_1')
        test_category_2 = Category.objects.create(name='test_category_2')
        institution = Institution.objects.create(name='test_institution', description='institution for test purpose')
        institution.categories.add(test_category_1, test_category_2)
        user = User.objects.create(first_name='user', last_name='user', username='user', email='user@email.com',
                                   password='top_secret')
        donation = Donation.objects.create(quantity=1, address='test_address', phone_number='1111', city='test_city',
                                           zip_code='11-000', pick_up_date='2020-06-22', pick_up_time='00:00',
                                           pick_up_comment='test_comment',
                                           user=user, institution=institution)
        donation.categories.add(test_category_1, test_category_2)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('charity:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('charity:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')