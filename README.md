# coffeemize
Coffeemize is an app that randomly shows to a logged-in user coffeeplaces  in Lviv. 

The project has two apps:

* Coffee places
* Accounts

## Coffee places
The Coffee places app has venues, obtained from https://foursquare.com/, which are proposed to the user according to random suggestions algorithm. The user's choices are saved so that suggestions won't be repeated.


## Accounts App

The Accounts app is a very simple and contains just a User model a bit changed for auth0 purposes.


## Technology Stack

- Python 3.5
- Django 1.10
- Django REST framework 3.5
- Angular 1.4

## Installation guideline

 - Activate your virtual environment: `source <virtual_env>/bin/activate`
 - Install needed packages: `pip install -r requirements.txt`
 - Syncdb: `python manage.py migrate`
 - Run Django server: `python manage.py runserver`
 - Run Frontend: `npm install`, `bower install`, `grunt serve`

Coffeemize frontend is here: https://github.com/kate-ka/coffeemize_frontend
