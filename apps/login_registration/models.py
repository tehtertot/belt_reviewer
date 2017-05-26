# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[A-Za-z\d+-._]+@[A-Za-z\d+-._]+.[A-Za-z]+$')

class UserManager(models.Manager):
    def login(self, postData):
        errors = []
        try:
            user = User.objects.get(email=postData['email'])
            if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) == user.password.encode():
                return user
            else:
                errors.append('Invalid password')
                return errors
        except:
            errors.append('No user with this password')
            return errors

    def register(self, postData):
        errors = []
        #name validation
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors.append('Invalid first name')
        if len(postData['last_name']) < 2 or not ln.isalpha():
            errors.append('Invalid last name')
        #email validation
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Invalid email')
        else:
            try:
                e = User.objects.get(email=postData['email'])
                errors.append('Email is associated with an existing user')
            except: #email not yet registered - OK
                pass
        #birthdate validation
        try:
            y, m, d = map(int, bd.split('-'))
            postData['birthdate'] = datetime(y, m, d)
            if postData['birthdate'] > datetime.now():
                errors.append('Invalid birthdate')
        except:
            errors.append('No birthdate entered')

        #password validation
        if postData['password'] != postData['confirm']:
            errors.append('Passwords do not match')
        if len(postData['password']) < 8:
            errors.append('Invalid password')

        #return new user if all fields valid
        if len(errors) == 0:
            hashedpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            newUser = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashedpw)
            return newUser
        #or return list of errors
        return errors
    # def resetPassword(self, id, pw):
    #     u = User.objects.get(id=id)
    #     u.salt = bcrypt.gensalt()
    #     u.password = bcrypt.hashpw(pw.encode(), u.salt)
    #     u.save()

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    birthdate = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.first_name + " " + self.last_name
