# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, HttpResponsePermanentRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Weather
from django.contrib.auth import authenticate, login
from util import weather
import time
from django.core import serializers


def email_validation(email):
    try:
        validate_email(email)
    except ValidationError as e:
        return 'You entered invalid email'
    else:
        return True


def password_confirm_validation(password1, password2):
    if password1 == password2:
        return True
    else:
        return 'Confirmation password and password need to match'


def show_index(request):
    return render(request, 'forecast_scrapping/show_index.html', {})


def show_login(request):
    if request.method == 'POST':

        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'forecast_scrapping/show_login.html',
                          {'error': 'All form input fields are required'})

        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            if user.is_active:
                request.session['logged_in'] = True
                request.session['username'] = user.username
                return HttpResponsePermanentRedirect('/weather')
            else:
                return render(request, 'forecast_scrapping/show_login.html', {'error': 'This account is disabled.'})
        else:
            return render(request, 'forecast_scrapping/show_login.html', {'error': 'Details entered do not exist.'})

    return render(request, 'forecast_scrapping/show_login.html', {})


def show_register(request):
    if request.method == 'POST':
        error_messages = []
        email = email_validation(request.POST['email'])
        passwords = password_confirm_validation(request.POST['password'], request.POST['confirm_password'])

        if request.POST['email'] == '' or request.POST['password'] == '' or request.POST['confirm_password'] == '':
            error_messages.append('All form input fields are required')
            return render(request, 'forecast_scrapping/show_register.html', {'errors': error_messages})

        if email is not True and passwords is not True:
            error_messages.append(email)
            error_messages.append(passwords)
            return render(request, 'forecast_scrapping/show_register.html', {'errors': error_messages})

        if passwords is not True or email is not True:
            error_messages.append(email)
            error_messages.append(passwords)
            return render(request, 'forecast_scrapping/show_register.html', {'errors': error_messages})

        # create user
        User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])

        return render(request, 'forecast_scrapping/show_login.html', {'message': 'Please login'})

    return render(request, 'forecast_scrapping/show_register.html', {})


def show_weather(request):
    if request.session.get('logged_in', False):

        weather_list = Weather.objects.all()
        paginator = Paginator(weather_list, 3)

        page = request.GET.get('page')

        try:
            weather = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            weather = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            weather = paginator.page(paginator.num_pages)

        return render(request, 'forecast_scrapping/show_weather.html', {'username': request.session['username'],
                                                                        'weather': weather})

    return HttpResponsePermanentRedirect('/login')


def api_weather(request, username, password):

    if username == '' or password == '':
        return JsonResponse({'error message': 'Authentication required'})

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            data = serializers.serialize('json', Weather.objects.all())
            return JsonResponse({'weather': data})
        else:
            return JsonResponse({'error message': 'This account is disabled.'})
    else:
        return JsonResponse({'error message': 'Details entered do not exist.'})


def get_api_weather(request):
    weather_list = weather.get_weather()

    for item in weather_list['list']:
        w = Weather.objects.create(date=time.strftime("%Y-%m-%d", time.localtime(int(item['dt']))),
                                   min_tem=item['temp']['min'], max_temp=item['temp']['max'],
                                   wind=item['speed'], rain=item['clouds'])
        w.save(force_insert=True)

    return HttpResponsePermanentRedirect('/logout')


def logout(request):
    del request.session['logged_in']
    del request.session['username']

    return HttpResponsePermanentRedirect('/')
