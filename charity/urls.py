from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
import django.contrib.auth.views as auth_views

from . views import LandingPage, AddDonation, Confirmation, Login, LogoutView,Register, Activate, UserView, EditUserData, DonationsView, DonationView

app_name = 'charity'

urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'), - zamiast tego to niżej
    #path('', TemplateView.as_view(template_name='budget/index.html'), name = 'index'),

    path('', LandingPage.as_view(), name='index'),
    path('add_donation', AddDonation.as_view(), name='add_donation'),
    path('confirmation', Confirmation.as_view(), name='confirmation'),
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', Register.as_view(), name='register'),
    path('activate/<str:uid>/<str:token>', Activate.as_view(), name='activate'),
    path('my_account', UserView.as_view(), name='my_account'),
    path('edit_user', EditUserData.as_view(), name='edit_user'),
    # path('password_reset', auth_views.PasswordResetView.as_view(template_name= 'registration/password_reset_form.html',
    #                         success_url=reverse_lazy('charity:password_reset_done')), name='password_reset'),
    # path('password_reset/done', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    # path('reset/<str:uid>/<str:token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('my_donations', DonationsView.as_view(), name='my_donations'),
    path('my_donations/<int:donation_id>', DonationView.as_view(), name='my_donation'),
    ]