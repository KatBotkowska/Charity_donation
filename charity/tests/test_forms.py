from django.forms import CharField, EmailField, IntegerField, ModelMultipleChoiceField, ModelChoiceField, DateField, \
    TimeField, BooleanField
from django.test import TestCase

from charity.forms import UserForm, EditUserForm, DonationForm, ContactForm
from django.contrib.auth.models import User
from charity.models import Category, Institution, Donation


class UserFormTest(TestCase):

    def test_name_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields['name'].label == 'Imię')

    def test_name_field_instance(self):
        form = UserForm()
        self.assertTrue(isinstance(form.fields['name'], CharField))

    def test_name_field_length(self):
        form = UserForm()
        max_length = form.fields['name'].max_length
        self.assertEquals(max_length, 128)

    def test_surname_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields['surname'].label == 'Nazwisko')

    def test_surname_field_instance(self):
        form = UserForm()
        self.assertTrue(isinstance(form.fields['surname'], CharField))

    def test_surname_field_length(self):
        form = UserForm()
        max_length = form.fields['surname'].max_length
        self.assertEquals(max_length, 128)

    def test_email_field_instance(self):
        form = UserForm()
        self.assertTrue(isinstance(form.fields['email'], EmailField))

    def test_password1_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields['password1'].label == 'Hasło')

    def test_password1_field_instance(self):
        form = UserForm()
        self.assertTrue(isinstance(form.fields['password1'], CharField))

    def test_password2_field_label(self):
        form = UserForm()
        self.assertTrue(form.fields['password2'].label, 'Powtórz hasło')

    def test_password2_field_instance(self):
        form = UserForm()
        self.assertTrue(isinstance(form.fields['password2'], CharField))

    def test_form_meta_fields(self):
        form = UserForm()
        expected_fields = ["name", "surname", "email", "password1", "password2"]
        self.assertTrue(form.fields, expected_fields)

    def test_form_save_method(self):
        data = {
            'name': ' testuser',
            'surname': 'testsurname',
            'email': 'emailtest@o2.pl',
            'password1': 'Secret_password1@',
            'password2': 'Secret_password1@'
        }
        form = UserForm(data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            user = form.save()
            self.assertTrue(User.objects.get(pk=user.pk).username, data['email'])
            self.assertTrue(User.objects.get(pk=user.pk).first_name, data['name'])
            self.assertTrue(User.objects.get(pk=user.pk).last_name, data['surname'])

    def test_form_clean_method(self):
        data1 = {
            'name': ' testuser',
            'surname': 'testsurname',
            'email': 'emailtest@o2.pl',
            'password1': 'Secret_password1@',
            'password2': 'Secret_password1@'
        }
        form1 = UserForm(data1)
        form1.save()
        data2 = {
            'name': ' next_testuser',
            'surname': 'next_testsurname',
            'email': 'emailtest@o2.pl',
            'password1': 'Secret_password1@',
            'password2': 'Secret_password1@'
        }
        form2 = UserForm(data2)
        self.assertFalse(form2.is_valid())
        self.assertEqual(form2.errors['__all__'], ['Email already in db'])


class EditUserFormTest(TestCase):

    def test_name_field_label(self):
        form = EditUserForm()
        self.assertTrue(form.fields['name'].label == 'Imię')

    def test_name_field_instance(self):
        form = EditUserForm()
        self.assertTrue(isinstance(form.fields['name'], CharField))

    def test_name_field_length(self):
        form = EditUserForm()
        max_length = form.fields['name'].max_length
        self.assertEquals(max_length, 128)

    def test_surname_field_label(self):
        form = EditUserForm()
        self.assertTrue(form.fields['surname'].label == 'Nazwisko')

    def test_surname_field_instance(self):
        form = EditUserForm()
        self.assertTrue(isinstance(form.fields['surname'], CharField))

    def test_surname_field_length(self):
        form = EditUserForm()
        max_length = form.fields['surname'].max_length
        self.assertEquals(max_length, 128)

    def test_email_field_instance(self):
        form = EditUserForm()
        self.assertTrue(isinstance(form.fields['email'], EmailField))

    def test_oldpassword_field_label(self):
        form = EditUserForm()
        self.assertTrue(form.fields['old_password'].label == 'Hasło')

    def test_oldpassword_field_instance(self):
        form = EditUserForm()
        self.assertTrue(isinstance(form.fields['old_password'], CharField))

    def test_newpassword1_field_label(self):
        form = EditUserForm()
        self.assertTrue(form.fields['new_password1'].label, 'Nowe hasło')

    def test_newpassword1_field_instance(self):
        form = EditUserForm()
        self.assertTrue(isinstance(form.fields['new_password1'], CharField))

    def test_newpassword2_field_label(self):
        form = EditUserForm()
        self.assertTrue(form.fields['new_password2'].label, 'Powtórz nowe hasło')

    def test_newpassword2_field_instance(self):
        form = EditUserForm()
        self.assertTrue(isinstance(form.fields['new_password2'], CharField))

    def test_form_meta_fields(self):
        form = EditUserForm()
        expected_fields = ["name", "surname", "email", "old_password", "new_password1", "new_password2"]
        self.assertTrue(form.fields, expected_fields)

    def test_form_save_method(self):
        original_data = {
            'name': ' testuser',
            'surname': 'testsurname',
            'email': 'emailtest@o2.pl',
            'password1': 'Secret_password1@',
            'password2': 'Secret_password1@'
        }
        form = UserForm(original_data)
        form.save()
        changed_data = {
            'name': ' newtestuser',
            'surname': 'newtestsurname',
            'email': 'newemailtest@o2.pl',
            'old_password': 'Secret_password1@',
            'new_password1': 'newSecret_password1@',
            'new_password2': 'newSecret_password1@'
        }
        new_form = EditUserForm(changed_data)
        self.assertTrue(new_form.is_valid())
        if new_form.is_valid():
            user = new_form.save()
            self.assertTrue(User.objects.get(pk=user.pk).username, changed_data['email'])
            self.assertTrue(User.objects.get(pk=user.pk).email, changed_data['email'])
            self.assertTrue(User.objects.get(pk=user.pk).first_name, changed_data['name'])
            self.assertTrue(User.objects.get(pk=user.pk).last_name, changed_data['surname'])

    def test_form_clean_method(self):
        data1 = {
            'name': ' testuser',
            'surname': 'testsurname',
            'email': 'emailtest@o2.pl',
            'password1': 'Secret_password1@',
            'password2': 'Secret_password1@'
        }
        form1 = UserForm(data1)
        form1.save()
        data1a = {
            'name': ' newtestuser',
            'surname': 'newtestsurname',
            'email': 'newemailtest@o2.pl',
            'password1': 'newSecret_password1@',
            'password2': 'newSecret_password1@'
        }
        form1a = UserForm(data1a)
        form1a.save()
        data2 = {
            'name': ' other_testuser',
            'surname': 'other_testsurname',
            'email': 'emailtest@o2.pl',
            'old_password': 'Secret_password2@',
            'new_password1': 'otherSecret_password1@',
            'new_password2': 'anySecret_password1@'
        }
        form2 = EditUserForm(data2)
        self.assertFalse(form2.is_valid())
        print(form2.errors)
        self.assertEqual(form2.errors['__all__'], ['Email already in db'])
        data2a = {
            'name': ' other_testuser',
            'surname': 'other_testsurname',
            'email': 'any_newemailtest@o2.pl',
            'old_password': 'newSecret_password1@',
            'new_password1': 'otherSecret_password1@',
            'new_password2': 'anySecret_password1@'
        }
        form2a = EditUserForm(data2a)
        print(form2a.errors)
        self.assertFalse(form2a.is_valid())  # TODO nie pasujące hasła

        self.assertEqual(form2a.errors['__all__'], ['Email already in db'])


class DonationFormTest(TestCase):

    def test_quantity_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['quantity'].label == 'Ilość')

    def test_quantity_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['quantity'], IntegerField))

    def test_categories_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['categories'].label == 'Kategorie darów')

    def test_categories_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['categories'], ModelMultipleChoiceField))

    def test_institution_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['institution'].label == 'Instytucja')

    def test_institution_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['institution'], ModelChoiceField))

    def test_address_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['address'].label == 'Adres')

    def test_address_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['address'], CharField))

    def test_address_field_length(self):
        form = DonationForm()
        max_length = form.fields['address'].max_length
        self.assertEquals(max_length, 256)


    def test_phone_number_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['phone_number'].label == 'Numer telefonu')

    def test_phone_number_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['phone_number'], CharField))

    def test_phone_number_field_length(self):
        form = DonationForm()
        max_length = form.fields['phone_number'].max_length
        self.assertEquals(max_length, 12)

    def test_city_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['city'].label == 'Miasto')

    def test_city_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['city'], CharField))

    def test_city_field_length(self):
        form = DonationForm()
        max_length = form.fields['city'].max_length
        self.assertEquals(max_length, 126)

    def test_zip_code_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['zip_code'].label == 'Kod pocztowy')

    def test_zip_code_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['zip_code'], CharField))

    def test_zip_code_field_length(self):
        form = DonationForm()
        max_length = form.fields['zip_code'].max_length
        self.assertEquals(max_length, 6)

    def test_pick_up_date_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['pick_up_date'].label == 'Data odbioru')

    def test_pick_up_date_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['pick_up_date'], DateField))

    def test_pick_up_time_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['pick_up_time'].label == 'Godzina odbioru')

    def test_pick_up_time_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['pick_up_time'], TimeField))

    def test_pick_up_comment_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['pick_up_comment'], CharField))

    def test_user_field_exists(self):
        form = DonationForm()
        self.assertFalse('user' in form.fields)

    def test_status_field_label(self):
        form = DonationForm()
        self.assertTrue(form.fields['status'].label == 'Czy dary odebrane?')

    def test_status_field_instance(self):
        form = DonationForm()
        self.assertTrue(isinstance(form.fields['status'], BooleanField))

    def test_update_date_field_exists(self):
        form = DonationForm()
        self.assertFalse('update_date' in form.fields)


class ContactFormTest(TestCase):

    def test_name_field_label(self):
        form = ContactForm()
        self.assertTrue(form.fields['name'].label == 'Imię')

    def test_name_field_instance(self):
        form = ContactForm()
        self.assertTrue(isinstance(form.fields['name'], CharField))

    def test_name_field_length(self):
        form = ContactForm()
        max_length = form.fields['name'].max_length
        self.assertEquals(max_length, 126)

    def test_surname_field_label(self):
        form = ContactForm()
        self.assertTrue(form.fields['surname'].label == 'Nazwisko')

    def test_surname_field_instance(self):
        form = ContactForm()
        self.assertTrue(isinstance(form.fields['surname'], CharField))

    def test_surname_field_length(self):
        form = ContactForm()
        max_length = form.fields['surname'].max_length
        self.assertEquals(max_length, 126)

    def test_message_field_label(self):
        form = ContactForm()
        self.assertTrue(form.fields['message'].label == 'Wiadomość')

    def test_message_field_instance(self):
        form = ContactForm()
        self.assertTrue(isinstance(form.fields['message'], CharField))



