from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django_registration.forms import RegistrationFormUniqueEmail


class UserForm(UserCreationForm):
    name = forms.CharField(max_length=128)
    surname = forms.CharField(max_length=128)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    #username = forms.TextInput(attrs= {'is_hidden': True})

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password1", "password2"]
        USERNAME_FIELD='email'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.name = self.cleaned_data["name"]
        user.surname = self.cleaned_data["surname"]
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