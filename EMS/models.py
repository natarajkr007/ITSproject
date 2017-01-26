from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    Address = models.CharField(max_length=250)
    phone_no=models.CharField(max_length=10)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username