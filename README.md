# Charity_donation
App for pass donations from people to NGO'S

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [To run](#to-run)


## General info:
App connects people that want to donate some items with NGO's that can help with passing them to those in need. 
* A registered user can donate items, selecting from categories, instututions (which can pick up all items), 
quantity, contact data, pickup time and place. 
* Form for adding donations made with JavaScript and JQuery.
* User can register with confirmation by email. User can change his data (after putting password), can reset password 
(with reset link in email confirmation).
* All emails send by Sendgrid API https://sendgrid.com/docs/for-developers/sending-email/api-getting-started/
* Admin site customised for polish users. Method delete_queryset for UserAdmin overrided for validation users count. 
User can't delete himself.
* Simple REST API for all models. Filters added. Authentication with Djoser library. Permissions: IsAuthenticatedOrReadOnly, for UserViewSet update with IsAuthenticated.




## Technologies

* asgiref==3.2.7
* confusable-homoglyphs==3.2.0
* Django==3.0.5
* django-registration==3.1
* psycopg2-binary==2.8.5
* python-decouple==3.3
* python-http-client==3.2.7
* pytz==2019.3
* sendgrid==6.3.0
* six==1.14.0
* sqlparse==0.3.1

## To run
* clone repository
* create virtual environment (virtualenv -p python3 venv) and activate it  (source venv/bin/activate)
* install requirements with pip install -r requirements.txt
* create database (I use PostgreSQL - check settings.py)
* make a first migration
* add random data for database
* run app: python manage.py runserver



