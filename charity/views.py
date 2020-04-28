from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.views import View
from .forms import UserForm
from . models import Donation, Institution, Category


def paginator(request, obj, num_per_page):
    # funkcja do paginowania stron
    # obj  - wynik zapytania sql wyświetlany na stronie
    # num_per_page - liczba wierszy z obiektu na stronie
    paginator = Paginator(obj, num_per_page)
    page = request.GET.get('page')
    try:
        obj_page = paginator.page(page)
    except PageNotAnInteger:
        obj_page = paginator.page(1)
    except EmptyPage:
        obj_page = paginator.page(paginator.num_pages)
    return obj_page


class LandingPage(View):
    def get(self, request):
        donations_quantity = Donation.objects.all().aggregate(total=Sum('quantity'))['total']
        institutions_supported = Institution.objects.filter(donation__quantity__isnull=False).distinct().count()
        institutions = Institution.objects.all()
        my_paginator = Paginator(institutions.filter(type='foundation'), 3)
        page_number = request.GET.get('page')
        foundations = my_paginator.get_page(page_number)
        #foundations = paginator(request, institutions.filter(type='foundation'), 3)
        ngos = paginator(request, institutions.filter(type='NGO'), 5)
        pick_ups = paginator(request, institutions.filter(type='local pick-up'), 5)
        return render(request, 'index.html', {'donations_quantity': donations_quantity,
                                              'institutions_supported':institutions_supported,
                                              'institutions':institutions,
                                              'foundations':foundations,
                                              'ngos':ngos,
                                              'pick_ups':pick_ups})

class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')

class Confirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

class Register(View):
    form_class = UserForm
    fields = '__all__'
    template_name = "register.html"


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('charity:index')
        else:
            messages.error(request, "Error")
            print('blad', form.error_messages)
            print(form.fields)
            print(form.data)
            print(form.cleaned_data)
        return render(request, self.template_name, {'form': form})


    #
    # def get(self, request):
    #     return render(request, 'register.html')