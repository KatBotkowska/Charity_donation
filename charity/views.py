from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import FormView, ListView, UpdateView, TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
import logging

logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
from .forms import UserForm, DonationForm, EditUserForm, ContactForm
from .models import Donation, Institution, Category
from .tokens import account_activation_token
from .authenticate_user import authenticate_user
from .sendgrid import sendgrid_account_message, sendgrid_contact_form

CHARITY_MY_ACCOUNT = 'charity:my_account'



def paginator(request, obj, num_per_page):
    # function for pages pagination
    # obj  - sql object displayed on page
    # num_per_page - rows number from obj displayed on page
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
        foundations = paginator(request, institutions.filter(type='foundation'), 3)
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


class Confirmation(View):
    template_name = 'form-confirmation.html'

    def get(self, request):
        return render(request, self.template_name)


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
            user.is_active = False
            user.save()
            mail_subject = 'Aktywacja konta w domenie Donation'
            current_site = get_current_site(request)
            to_email = form.cleaned_data.get('email')
            email_template = 'acc_active_email.html'
            # send message by sendgrid:
            sendgrid_account_message(mail_subject, current_site, user, to_email, email_template, activate=True)

            return render(request, 'confirm_email.html')

        return render(request, self.template_name, {'form': form})


class Activate(View):
    def get(self, request, uid, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('charity:index')
        else:
            return HttpResponse('Activation link is invalid!')


class UserView(View):
    template_name = 'my_account.html'

    def get(self, request):
        donations = Donation.objects.filter(user=request.user)
        return render(request, self.template_name, {'donations': donations})


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
        return reverse(CHARITY_MY_ACCOUNT)

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
            if user is not None and user.is_active:
                login(self.request, user)
            return redirect(CHARITY_MY_ACCOUNT)
        return redirect(CHARITY_MY_ACCOUNT)


class MyPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    form_class = PasswordResetForm
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    token_generator = default_token_generator

    def get_success_url(self):
        return reverse('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = list(form.get_users(email))
        if users:
            for user in users:
                mail_subject = 'Link resetujacy konto'
                current_site = get_current_site(self.request)
                to_email = form.cleaned_data.get('email')
                email_template = 'registration/password_reset_email.html'
                # send message by sendgrid:
                sendgrid_account_message(mail_subject, current_site, user, to_email, email_template, reset=True)
                return redirect('password_reset_done')
        else:
            return redirect('password_reset_done')

    def form_invalid(self, form):
        return redirect('password_reset_done')


class DonationsView(ListView):
    template_name = 'donations.html'
    model = Donation
    context_object_name = 'donations'

    def get_queryset(self):
        donations = Donation.objects.filter(user=self.request.user)
        return donations


class DonationView(UpdateView):
    template_name = 'donation.html'
    model = Donation
    context_object_name = 'donation'
    fields = ('status',)
    pk_url_kwarg = 'donation_id'

    def get_success_url(self):
        return reverse('charity:my_donation', kwargs={'donation_id': self.object.id})


class ContactFormView(TemplateView):
    template_name = 'contact_form-confirmation.html'

    def post(self, request):
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            mail_subject = 'Nowa wiadomość z formularza kontaktowego'
            to_emails = [user.email for user in User.objects.filter(is_staff=True)]
            name = contact_form.cleaned_data['name']
            surname = contact_form.cleaned_data['surname']
            message = contact_form.cleaned_data['message']
            email_template = 'from_contact_form_email.html'
            # send message by sendgrid
            sendgrid_contact_form(mail_subject, to_emails, name, surname, message, email_template)
            return render(request, 'contact_form-confirmation.html')
