from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from Donation.settings import SENDGRID_API_KEY

SENDGRID_REGISTRED_EMAIL = 'katarzyna.botkowska@gmail.com'
import logging

logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
from .forms import UserForm, DonationForm, EditUserForm, ContactForm
from .models import Donation, Institution, Category
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from .authenticate_user import authenticate_user


def sendgrid_send(message):
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
    except Exception as e:
        logging.warning(e.message)


def sendgrid_account_message(mail_subject, current_site, user, to_email, email_template, activate=False, reset=False):
    mail_subject = mail_subject
    current_site = current_site
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    if activate:
        token = account_activation_token.make_token(user)
    if reset:
        token = default_token_generator.make_token(user)
    to_email = to_email
    text_to_send = render_to_string(email_template, {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    })
    message = Mail(
        from_email=SENDGRID_REGISTRED_EMAIL,
        to_emails=to_email,
        subject=mail_subject,
        html_content=text_to_send)
    sendgrid_send(message)


def sendgrid_contact_form(mail_subject, to_emails, name, surname, message, email_template):
    mail_subject = mail_subject
    to_emails = to_emails
    name = name
    surname = surname
    message = message
    text_to_send = render_to_string(email_template, {
        'name': name,
        'surname': surname,
        'message': message,
    })
    message = Mail(
        from_email=SENDGRID_REGISTRED_EMAIL,
        to_emails=to_emails,
        subject=mail_subject,
        html_content=text_to_send)
    sendgrid_send(message)
