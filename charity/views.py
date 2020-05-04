from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
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
from django.views.generic import FormView, ListView, DetailView, UpdateView

from .forms import UserForm, DonationForm, EditUserForm
from .models import Donation, Institution, Category


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
        # foundations = paginator(request, institutions.filter(type='foundation'), 3)
        ngos = paginator(request, institutions.filter(type='NGO'), 5)
        pick_ups = paginator(request, institutions.filter(type='local pick-up'), 5)
        return render(request, 'index.html', {'donations_quantity': donations_quantity,
                                              'institutions_supported': institutions_supported,
                                              'institutions': institutions,
                                              'foundations': foundations,
                                              'ngos': ngos,
                                              'pick_ups': pick_ups})


class AddDonation(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('charity:login')
    success_url = reverse_lazy('charity:confirmation')
    form_class = DonationForm

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        form = DonationForm(initial={'user': request.user})
        return render(request, 'form.html', {'form': form, 'categories': categories, 'institutions': institutions})

    def form_valid(self, form):
        donation = form.save(commit=False)
        donation.user = self.request.user
        donation.save()
        form.save_m2m()
        self.success_url = reverse('charity:confirmation')
        return HttpResponseRedirect(self.success_url)
    # def post(self, request):
    #     form = DonationForm(request.POST)
    #     print(form.fields)
    #     if form.is_valid():
    #         donation = form.save(commit=False)
    #         donation.user = request.user
    #         donation.save()
    #         form.save_m2m()
    #         return redirect('charity:confirmation')
    #     else:
    #         print(form.errors)
    #         form = DonationForm(initial={'user': request.user})
    #         categories = Category.objects.all()
    #         institutions = Institution.objects.all()
    #     return render(request, 'form.html', {'form': form, 'categories': categories, 'institutions': institutions})


class Confirmation(View):
    template_name = 'form-confirmation.html'
    def get(self, request):
        return render(request, self.template_name)


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
        user = authenticate_user(email, password)
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

class UserView(View):
    template_name = 'my_account.html'

    def get(self, request):
        return render(request, self.template_name)


class EditUserData(UpdateView):
    template_name = 'edit_user.html'
    model = User
    context_object_name = 'user'
    form_class = EditUserForm

    def get(self, request, *args, **kwargs):
        user = request.user
        initial = {'name': user.first_name, 'surname': user.last_name,
                   'email': user.email}
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('charity:my_account')

    def form_valid(self, form):
        user = form.save(commit=False)
        if 'email' in form.cleaned_data:
            username = form.cleaned_data['email']
        if 'new_password1' in form.cleaned_data and 'new_password2' in form.cleaned_data:
            password = form.cleaned_data['new_password1']
            user.set_password(password)
        user.save()
        if 'email' in form.cleaned_data or 'new_password1' in form.cleaned_data:
            username = form.cleaned_data['email']
            user = authenticate(username=username, password=form.cleaned_data['new_password1'])
            if user is not None:
                if user.is_active:
                    login(self.request, user)
            return redirect('charity:my_account')
        return redirect('charity:my_account')


class DonationsView(ListView):
    template_name='donations.html'
    model = Donation
    context_object_name = 'donations'

    def get_queryset(self):
        donations =Donation.objects.filter(user=self.request.user)
        return donations

class DonationView(UpdateView):
    template_name = 'donation.html'
    model = Donation
    context_object_name = 'donation'
    fields = ('status',)
    pk_url_kwarg = 'donation_id'

    def get_success_url(self):
        return reverse('charity:my_donation', kwargs={'donation_id': self.object.id})