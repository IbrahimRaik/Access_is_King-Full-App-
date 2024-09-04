from django.db import models
from django.utils.translation import gettext_lazy as _
from user_auth.models import User

class City(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    countryname = title = models.CharField(max_length=1024, default=None)
    title = models.CharField(max_length=1024)
    label = models.ImageField(upload_to='City/Images', blank=True)
    subtitle = models.CharField(max_length=256)
    members = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NewComments(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    comments = models.CharField(max_length=1024, blank=True)
    media_files = models.ImageField(upload_to='comment/Images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comments
    

class NewMessages(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24, unique=True)
    new_message = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.new_message