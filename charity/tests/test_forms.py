from django.forms import CharField, EmailField
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
            'old_password':'Secret_password2@',
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
        self.assertFalse(form2a.is_valid()) #TODO

        self.assertEqual(form2a.errors['__all__'], ['Email already in db'])





