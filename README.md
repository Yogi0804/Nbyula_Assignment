# Nbyula_Assignment

# Meet

## \_Schedule Meet with terraformers

Meet is a django based application for making schedule

## Features

- user can see all appointments
- user can see all upcoming appointment
- user can schedule an appointment
- can register users
- user can update their profile
- user can set off hours
- generate token of authentication
- generate refresh token for authentication

## Tech

- [Django](https://www.djangoproject.com)
- [Django-Rest-framework](https://www.django-rest-framework.org)

## Routes

```sh
        'GET': '/api/allAppointments/'
        'GET': '/api/upcomingAppointment/'
        'POST': '/api/scheduleAppointment/'
        'POST': '/api/register/'
        'POST': '/api/UpdateProfile/id/'
        'POST': '/api/offHours/'

        'POST': '/api/token/'
        'POST': '/api/token/refresh/'
```

## Installation

having a virtual environment is good and in python3 we can do something like

```sh
python3 -m venv env
source env/bin/activate 'activate virtual environment for mac and linux machine'
pip install django
django-admin startproject <your-project-name> .
```

## Postman

## Deployed

- [Meet-terraformers](https://meet-terraformers.herokuapp.com)

> Note: `add /api/ in the end of routes` is required for Routes.
