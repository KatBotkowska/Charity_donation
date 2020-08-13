from datetime import date, datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from charity.models import Category, Institution, Donation
from charity.forms import DonationForm
from charity.sendgrid import sendgrid_account_message, sendgrid_contact_form


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
        institution.categories.add(test_category_1)
        institution.categories.add(test_category_2)
        institution.save()
        test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                             email='user@email.com',
                                             password='Top_secret@1')
        test_user.save()
        donation = Donation.objects.create(quantity=1, address='test_address', phone_number='1111', city='test_city',
                                           zip_code='11-000', pick_up_date='2020-06-22', pick_up_time='00:00',
                                           pick_up_comment='test_comment',
                                           user=test_user, institution=institution)
        donation.categories.add(test_category_1)
        donation.categories.add(test_category_2)
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

    def test_redirect_to_confirmation_after_succes_form(self):  # TODO
        self.client.login(username='test_username', password='Top_secret@1')
        # post = {'categories':"5", 'quantity':"1", 'institution':'4', "address":'address', 'city':"wroclaw",
        #         'zip-code':"20-344", 'phone-number':'3322', 'pick-up-date':'2020-12-12', 'pick_up_time':'12:00',
        #         'user':'test_user'}
        # test_category_1 = Category.objects.create(name='test_category_1')
        # test_category_2 = Category.objects.create(name='test_category_2')
        # test_category_1.save()
        # test_category_2.save()
        cat_1 = Category.objects.first()
        cat_2 = Category.objects.get(name='test_category_2')
        inst = Institution.objects.first()
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
        errors = form.errors
        response = self.client.post(reverse('charity:add_donation'), data, follow=True)
        self.assertRedirects(response, reverse('charity:confirmation'), status_code=302, target_status_code=200)


class ConfirmationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(first_name='user', last_name='user', username='test_username',
                                             email='user@email.com',
                                             password='Top_secret@1')
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('charity:confirmation'))
        self.assertRedirects(response, '/login?next=%2Fconfirmation')

    def test_logged_in_view_url_exists_at_desired_location(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get('/confirmation')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_url_accessible_by_name(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('charity:confirmation'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_view_uses_correct_template(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('charity:confirmation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form-confirmation.html')

    def test_logged_in_user(self):
        self.client.login(username='test_username', password='Top_secret@1')
        response = self.client.get(reverse('charity:confirmation'))
        self.assertEqual(str(response.context['user']), 'test_username')


class LoginViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('charity:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('charity:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class LogoutViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('charity:logout'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('charity:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class RegisterViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('charity:register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('charity:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_view_post_success(self):  # TODO
        data = {
            'name': ' testuser',
            'surname': 'testsurname',
            'email': 'emailtest@o2.pl',
            'password1': 'Secret_password1@',
            'password2': 'Secret_password1@'
        }
        response = self.client.post(reverse('charity:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    # TODO sending email by sendgrid plus if failure - not sending

    def test_registration_view_post_failure(self):
        data = {
            'name': ' testuser',
            'surname': 'testsurname',
            'email': 'emailtest@o2.pl',
            'password1': 'Secret_password1@',
            'password2': 'Secret'
        }
        response = self.client.post(reverse('charity:register'), data)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='password2',
                             errors="Hasła w obu polach nie są zgodne.")


class ActivateViewTest(TestCase):  # TODO with registration view
    pass
    # def test_url_exists_at_desired_location(self):
    #     response = self.client.get('/activate')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_url_accessible_by_name(self):
    #     response = self.client.get(reverse('charity:activate'))
    #     self.assertEqual(response.status_code, 200)

    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('charity:activate'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'register.html')


class UserViewTest(TestCase):
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

    def test_url_exists_at_desired_location(self):
        login = self.client.login(username='user', password='top_secret')
        response = self.client.get('/my_account')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('charity:my_account'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('charity:my_account'))
        self.assertTemplateUsed(response, 'my_account.html')

    def test_view_return_donations(self):
        self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('charity:my_account'))
        self.assertEqual(len(response.context['donations']), 1)


class EditUserDataViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(first_name='user', last_name='user', username='user', email='user@email.com',
                                        password='top_secret')

    def test_url_exists_at_desired_location(self):
        login = self.client.login(username='user', password='top_secret')
        response = self.client.get('/edit_user')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('charity:edit_user'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('charity:edit_user'))
        self.assertTemplateUsed(response, 'edit_user.html')

    def test_form_initial_values(self):
        self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('charity:edit_user'))
        initial = {'name': 'user', 'surname': 'user', 'email': 'user@email.com'}
        self.assertEqual(response.context['form'].initial, initial)

    def test_update_data_with_redirect(self):
        user = User.objects.first()
        self.client.login(username='user', password='top_secret')
        updated_data = {'name': 'new_user', 'surname': 'New_user', "email": 'new_user@email.com',
                        "old_password": 'top_secret',
                        "new_password1": 'top_secret1', 'new_password2': 'top_secret1'}
        response = self.client.post(reverse('charity:edit_user'), updated_data)
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'new_user')
        self.assertEqual(user.last_name, 'New_user')
        self.assertEqual(user.email, 'new_user@email.com')
        self.assertEqual(user.username, 'new_user@email.com')
        self.assertEquals(user.check_password("top_secret1"), True)
        self.assertRedirects(response, reverse('charity:my_account'), status_code=302, target_status_code=200)


class MyPasswordResetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(first_name='user', last_name='user', username='user', email='user@email.com',
                                        password='top_secret')

    def test_url_exists_at_desired_location(self):
        login = self.client.login(username='user', password='top_secret')
        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='user', password='top_secret')
        response = self.client.get(reverse('password_reset'))
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')

    def test_post_data(self):
        self.client.login(username='user', password='top_secret')
        response = self.client.post(reverse('password_reset'), {'email': 'user@email.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('password_reset_done'), status_code=302, target_status_code=200)


class DonationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category_1 = Category.objects.create(name='test_category_1')
        test_category_2 = Category.objects.create(name='test_category_2')
        institution = Institution.objects.create(name='test_institution',
                                                 description='institution for test purpose')
        institution.categories.add(test_category_1, test_category_2)
        user = User.objects.create_user(first_name='user', last_name='user', username='user',
                                        email='user@email.com',
                                        password='top_secret')
        donation = Donation.objects.create(quantity=1, address='test_address', phone_number='1111',
                                           city='test_city',
                                           zip_code='11-000', pick_up_date='2020-06-22', pick_up_time='00:00',
                                           pick_up_comment='test_comment',
                                           user=user, institution=institution)
        donation.categories.add(test_category_1, test_category_2)


    def test_url_exists_at_desired_location(self):
        login = self.client.login(username='user', password='top_secret')
        donation = Donation.objects.first()
        response = self.client.get(f'/my_donations/{donation.id}')
        self.assertEqual(response.status_code, 200)


    def test_url_accessible_by_name(self):
        login = self.client.login(username='user', password='top_secret')
        donation = Donation.objects.first()
        response = self.client.get(reverse('charity:my_donation', kwargs={'donation_id': donation.id}))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        self.client.login(username='user', password='top_secret')
        donation = Donation.objects.first()
        response = self.client.get(reverse('charity:my_donation', kwargs={'donation_id': donation.id}))
        self.assertTemplateUsed(response, 'donation.html')

    def test_update_status_donation(self):
        self.client.login(username='user', password='top_secret')
        donation = Donation.objects.first()
        response = self.client.post(reverse('charity:my_donation', kwargs={'donation_id': donation.id}), {'status':True})
        self.assertEqual(response.status_code, 302)
        donation.refresh_from_db()
        self.assertEqual(donation.status, True)
        self.assertEquals(donation.update_date, date.today())
        self.assertRedirects(response, reverse('charity:my_donation', kwargs={'donation_id': donation.id}), status_code=302, target_status_code=200)

class ContactFormViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get('/process_contact_form')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('charity:contact_form_view'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('charity:contact_form_view'))
        self.assertTemplateUsed(response, 'contact_form-confirmation.html')
