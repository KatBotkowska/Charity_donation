from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django_registration.forms import RegistrationFormUniqueEmail

from .models import Donation


class UserForm(UserCreationForm):
    name = forms.CharField(max_length=128, label='Imię')
    surname = forms.CharField(max_length=128, label='Nazwisko')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')


    class Meta:
        model = User
        fields = ["name", "surname", "email", "password1", "password2"]
        USERNAME_FIELD='email'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"]
        user.last_name = self.cleaned_data["surname"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return cleaned_data
        raise forms.ValidationError('Email already in db')


class EditUserForm(ModelForm):
    name = forms.CharField(max_length=128, required=False, label='Imię')
    surname = forms.CharField(max_length=128, required=False, label='Nazwisko')
    email = forms.EmailField(required=True)
    old_password = forms.CharField(widget=forms.PasswordInput, required=True, label='Hasło')
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False, label='Nowe hasło')
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False, label='Powtórz nowe hasło')

    class Meta:
        model = User
        fields = ["name", "surname", "email", "old_password", "new_password1", "new_password2"]
        USERNAME_FIELD = 'email'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"]
        user.last_name = self.cleaned_data["surname"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        if 'email' in self.changed_data:
            email = cleaned_data.get('email')
            try:
                User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                return cleaned_data
            raise forms.ValidationError('Email already in db')
        if 'new_password1' in self.changed_data and 'new_password2' in self.changed_data:
            if cleaned_data.get('new_password1') != cleaned_data.get('new_password2'):
               raise forms.ValidationError('Changed passwords don\'t mach')
            return cleaned_data



class DonationForm(ModelForm):
    pick_up_comment = forms.CharField(widget=forms.Textarea(attrs={'rows': '4'}), required=False)
    class Meta:
        model = Donation
        exclude = ('user',)



