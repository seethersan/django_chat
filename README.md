# django chat

Django Chat app with channels

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Run backend

Running the following command:

    $ docker-compose -f local.yml up -d

### Create superuser

Connect to the django_chat_local_django

Export DATABASE URL

    $ export DATABASE_URL="postgres://ASyaeeLtZMdFPOAglHFjgPMvlPhSdwTK:qGAAW9nGnvA4wfb9TZWioLbQ6SY5MFk0p7dUN6OUSgShdTn7jlhdv8dTbEnvN12i@postgres:5432/django_chat"

Set CELERY_BROKER_URL

    $ export CELERY_BROKER_URL="redis://redis:6379/0"

Then you can create super user

    $ python manage.py createsuperuser

### Create patients and doctors

Now this chat connect doctors and patients assigned to them. So in Chat link patients can only see online the doctors that are treating them and viceversa.

Using this URL http://127.0.0.1:8000/accounts/signup/ you now can register both patients and doctors, and you can assign patients to doctors using DJANGO Admin.

### Run frontend

Running the following commands:

    $ cd frontend/
    $ npm start

The frontend runs in http://localhost:3000
