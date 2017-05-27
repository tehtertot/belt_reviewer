# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from datetime import datetime

def index(request):
    return render(request, 'login_registration/index.html')

def login(request):
    if request.method=="POST":
        user = User.objects.login(request.POST)
        if isinstance(user, list):
            for error in user:
                messages.add_message(request, messages.INFO, error, extra_tags="login")
            return redirect('login:index')
        else:
            setSessionVars(request, user)
            return redirect('books:index')
    return redirect('login:index')

def register(request):
    if request.method=="POST":
        user = User.objects.register(request.POST)
        if isinstance(user, list):
            for error in user:
                messages.add_message(request, messages.INFO, error, extra_tags="reg")
            return redirect('login:index')
        else:
            setSessionVars(request, user)
            return redirect('books:index')
    return redirect('login:index')

def success(request):
    return render(request, 'login_registration/success.html')

def setSessionVars(request, user):
    request.session['name'] = user.first_name
    request.session['user_id'] = user.id

def logout(request):
    request.session.pop('name')
    request.session.pop('user_id')
    return redirect('login:index')
