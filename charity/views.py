from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

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

class AddDonation(LoginRequiredMixin, View):
    login_url = reverse_lazy('charity:login')


    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        #categories_selected =
        return render(request, 'form.html', {'categories':categories, 'institutions':institutions})

    def post(self,request):
        return reverse_lazy('charity:confirmation')

class Confirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')



def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None

class Login(LoginView):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user= authenticate_user(email, password)
        context = {}

        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return redirect('charity:index')
            else:
                context['error message'] = 'user is not active'
        else:
            return redirect('charity:register')
        return render(request, self.template_name, context)


    # def get_success_url(self):
    #     self.success_url = reverse('charity:index')
    #     return self.success_url
    #
    # def form_valid(self, form):
    #     """Security check complete. Log the user in."""
    #     login(self.request, form.get_user())
    #     return HttpResponseRedirect(self.get_success_url())

class LogoutView(LogoutView):
    template_name = 'index.html'



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

        return render(request, self.template_name, {'form': form})


