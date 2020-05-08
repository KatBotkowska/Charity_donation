from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
# sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

SENDGRID_API_KEY = config('SENDGRID_API_KEY')

# Create your views here.
from django.views import View
from django.views.generic import FormView, ListView, DetailView, UpdateView, TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from .forms import UserForm, DonationForm, EditUserForm, ContactForm
from .models import Donation, Institution, Category
from .tokens import account_activation_token


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
            user.is_active = False
            user.save()
            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
            #         return redirect('charity:index')
            mail_subject = 'Aktywacja konta w domenie Donation'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            # activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
            to_email = form.cleaned_data.get('email')
            text_to_send = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            message = Mail(
                from_email='katarzyna.botkowska@gmail.com',
                to_emails=to_email,
                subject=mail_subject,
                html_content=text_to_send)
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)

            # message = render_to_string('acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # message = "Hello {0},\nyour acctivation link: {1}".format(user.username, activation_link)
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()
            return render(request, 'confirm_email.html')
            # return HttpResponse('Please confirm your email address to complete the registration')

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
            # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
            # return render(request, 'activation.html')
            # form = PasswordChangeForm(request.user)
            # return render(request, 'activation.html', {'form': form})
        else:
            return HttpResponse('Activation link is invalid!')

    # def post(self, request):
    #     form = PasswordChangeForm(request.user, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user) # Important, to update the session with the new password
    #         return HttpResponse('Password changed successfully')


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


class MyPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    # form_class = MyPasswordResetForm
    form_class = PasswordResetForm
    from_email = 'katarzyna.botkowska@gmail.com'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    token_generator = default_token_generator

    def get_success_url(self):
        return reverse('password_reset_done')

    def form_valid(self, form):
        # super().form_valid(form)
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        email = form.cleaned_data['email']
        users = list(form.get_users(email))
        if users:
            for user in users:
                mail_subject = 'Link resetujacy konto'
                current_site = get_current_site(self.request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                to_email = form.cleaned_data.get('email')
                text_to_send = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                message = Mail(
                    from_email='katarzyna.botkowska@gmail.com',
                    to_emails=to_email,
                    subject=mail_subject,
                    html_content=text_to_send)
                try:
                    sg = SendGridAPIClient(SENDGRID_API_KEY)
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e.message)
                return redirect('password_reset_done')
        else:
            return redirect('password_reset_done')

    def form_invalid(self, form):
        return redirect('password_reset_done')

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data()
    #     ctx['uid'] =


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

    # def get(self, request):
    #     contact_form = ContactForm()
    #     return {'contact_form': contact_form}

    def post(self, request):
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            mail_subject = 'Nowa wiadomość z formularza kontaktowego'
            to_emails = [user.email for user in User.objects.filter(is_staff=True)]
            name = contact_form.cleaned_data['name']
            surname = contact_form.cleaned_data['surname']
            message = contact_form.cleaned_data['message']
            text_to_send = render_to_string('from_contact_form_email.html', {
                'name': name,
                'surname': surname,
                'message': message,
            })
            message = Mail(
                from_email='katarzyna.botkowska@gmail.com',
                to_emails=to_emails,
                subject=mail_subject,
                html_content=text_to_send)
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)

            return render(request, 'contact_form-confirmation.html')
            # next = request.POST.get('next')
            # return redirect(next)
