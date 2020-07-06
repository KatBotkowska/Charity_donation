from datetime import date, datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from charity.models import Category, Institution, Donation
from charity.forms import DonationForm

class LandingPageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category_1 = Category.objects.create(name='test_category_1')
        test_category_2 = Category.objects.create(name='test_category_2')
        institution = Institution.objects.create(name='test_institution', description='institution for test purpose')
        institution.categories.add(test_category_1, test_category_2)
        user = User.objects.create_user(first_name='user', last_name='user', username='user', email='user@email.com',
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

class AddDonationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category_1 = Category.objects.create(name='test_category_1')
        test_category_2 = Category.objects.create(name='test_category_2')
        institution = Institution.objects.create(name='test_institution', description='institution for test purpose')
        institution.categories.add(test_category_1, test_category_2)
        test_user = User.objects.create_user(first_name='user', last_name='user', username ='test_username', email='user@email.com',
                                   password='Top_secret@1')
        test_user.save()
        donation = Donation.objects.create(quantity=1, address='test_address', phone_number='1111', city='test_city',
                                           zip_code='11-000', pick_up_date='2020-06-22', pick_up_time='00:00',
                                           pick_up_comment='test_comment',
                                           user=test_user, institution=institution)
        donation.categories.add(test_category_1, test_category_2)
        donation.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('charity:add_donation'))
        self.assertRedirects(response, '/login?next=%2Fadd_donation')

    def test_logged_in_view_url_exists_at_desired_location(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get('/add_donation')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_url_accessible_by_name(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('charity:add_donation'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_uses_correct_template(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('charity:add_donation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_logged_in_user(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('charity:add_donation'))
        self.assertEqual(str(response.context['user']), 'test_username')

    def test_redirect_to_confirmation_after_succes_form(self):
        self.client.login(username='test_username', password='Top_secret@1')
        # post = {'categories':"5", 'quantity':"1", 'institution':'4', "address":'address', 'city':"wroclaw",
        #         'zip-code':"20-344", 'phone-number':'3322', 'pick-up-date':'2020-12-12', 'pick_up_time':'12:00',
        #         'user':'test_user'}
        # test_category_1 = Category.objects.create(name='test_category_1')
        # test_category_2 = Category.objects.create(name='test_category_2')
        # test_category_1.save()
        # test_category_2.save()
        cat_1 = Category.objects.get(name='test_category_1')
        cat_2 = Category.objects.get(name='test_category_2')
        inst = Institution.objects.get(name='test_institution')
        us = User.objects.get(username='test_username')
        # institution = Institution.objects.create(name='test_institution', description='institution for test purpose')
        # institution.categories.add(test_category_1, test_category_2)
        # institution.save()
        #
        # user = User.objects.create(first_name='user', last_name='user', username='user', email='user@email.com',
        #                            password='top_secret')

        data = {
            'quantity': 1, 'address': 'test_address', 'phone_number': '1111', 'city': 'test_city',
            "zip_code": '11-000', 'pick_up_date': date.today(), 'pick_up_time': datetime.now().time(),
            "pick_up_comment": 'test_comment', 'categories': [cat_2],
            'institution': inst, "user": us
        }
        form = DonationForm(data)
        response = self.client.post(reverse('charity:add_donation'), data, follow=True)
        self.assertRedirects(response, reverse('charity:confirmation'), status_code=302, target_status_code=200)

