from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICE = (
        ('C', 'Customer'),
        ('O', 'Official'),
    )
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    address = models.CharField(max_length=10, null=False, blank=False)
    phone_no=models.CharField(max_length=10, null=False, blank=False)
    role = models.CharField(max_length=1, default="C", choices=ROLE_CHOICE)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username



class Energy(models.Model):
    serviceno=models.CharField(max_length=10, null=False, blank=False)
    consumption=models.CharField(max_length=10, null=False, blank=False)
    timestamp = models.CharField(max_length=50,null=False,blank=False)

    def __str__(self):
        return self.serviceno
        
