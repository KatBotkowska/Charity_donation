import django
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import render_to_string


from .forms import ContactForm

def global_contact_form(request):
    return {'contact_form': ContactForm()}

