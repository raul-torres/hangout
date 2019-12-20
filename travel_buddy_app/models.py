from django.db import models
import bcrypt
from datetime import datetime

# Create your models here.
class userManager(models.Manager):
    def registration_validator(self, postdata):
        errors = {}
        if len(postdata['name']) < 3:
            errors['name_len'] = 'Your name has to be longer than 2 characters.'
        user_matcher = User.objects.filter(user_name = postdata['user_name'])
        if len(user_matcher) > 0:
            errors['user_matcher'] = 'User name is already taken.'
        if len(postdata['user_name']) < 3:
            errors['user_name_len'] = 'The user name has to be longer than 2 characters.'
        if len(postdata['password']) < 10:
            errors['password_len'] = 'The password has to be greater than 10 characters'
        if postdata['password'] != postdata['confirm_password']:
            errors['password_matcher'] = 'The passwords do not match. Please try again.'
        return errors
    
    def login_validator(self, postdata):
        errors = {}
        user_matcher = User.objects.filter(user_name = postdata['user_name'])
        if len(user_matcher) < 1:
            errors['invalid_user_name'] = 'Please check user name and try again'
        else:
            password_check = user_matcher[0]
            if bcrypt.checkpw(postdata['password'].encode(),    password_check.password.encode()):
                print('______________ACC3$$________GRANT3D________')
            else:
                errors['invalid_password'] = 'Please check password and try again'
        return errors

    def trip_validator(self, postdata):
        errors = {}
        if len(postdata['destination']) < 1:
            errors['destination_len'] = 'Destination cannot be empty.'
        if len(postdata['desc']) < 1:
            errors['desc_len'] = 'Description cannot be empty.'
        today = datetime.now()
        if postdata['travel_date_from'] < str(today):
            errors['travel_date_from_in_past'] = 'The Travel Date From must be in the future.'
        if postdata['travel_date_to'] < postdata['travel_date_from']:
            errors['travel_date_to_confusion'] = 'The Travel Date To cannot be before the Travel Date From'
        if postdata['travel_date_to'] < str(today):
            errors['travel_date_to_in_past'] = 'The Travel Date To must be in the future.'
        return errors

    # def communication_validator(self, postdata):
    #     errors = {}


class User(models.Model):
    name = models.CharField(max_length = 255)
    user_name = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    address = models.TextField(default = None)
    status = models.TextField(default = 'pending')
    notes = models.TextField(default = '')
    desc = models.TextField()
    travel_date_to = models.DateTimeField()
    travel_date_from = models.DateTimeField()
    planned_by = models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    users_joining = models.ManyToManyField(User, related_name='users_joined')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='messages', on_delete = models.CASCADE)
    trip = models.ForeignKey(Trip, related_name='trips', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = userManager()