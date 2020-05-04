from  django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'charity'

urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'), - zamiast tego to niżej
    #path('', TemplateView.as_view(template_name='budget/index.html'), name = 'index'),

    path('', views.LandingPage.as_view(), name='index'),
    path('add_donation', views.AddDonation.as_view(), name='add_donation'),
    path('confirmation', views.Confirmation.as_view(), name='confirmation'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('activate/<str:uid>/<str:token>', views.Activate.as_view(), name='activate'),
    path('my_account', views.UserView.as_view(), name='my_account'),
    path('edit_user', views.EditUserData.as_view(), name='edit_user'),
    path('my_donations', views.DonationsView.as_view(), name='my_donations'),
    path('my_donations/<int:donation_id>', views.DonationView.as_view(), name='my_donation'),
    ]