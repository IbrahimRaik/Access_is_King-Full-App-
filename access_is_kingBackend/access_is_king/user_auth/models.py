from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, phone=None, auth_provider=None, auth_token=None, bid=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            auth_provider=auth_provider,
            auth_token=auth_token,
            bid=bid  # Assign the BID number
        )
        user.code = uuid.uuid4().hex[:6].upper()
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class BIDNumber(models.Model):
    bid = models.CharField(max_length=6, unique=True)  # Unique 6-digit BID number
    is_used = models.BooleanField(default=False)  # Track if the BID has been used

    def __str__(self):
        return self.bid


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=24)
    name = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256, default="", blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.CharField(max_length=1024, blank=True, null=True)
    remember_token = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_token = models.CharField(max_length=256, default="", blank=True)
    auth_provider = models.CharField(max_length=255, default="", blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    terms_conditions = models.BooleanField(default=True)
    login_mode = models.CharField(max_length=256, default='Email')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bid = models.ForeignKey(BIDNumber, on_delete=models.SET_NULL, null=True, blank=True)  # Link BID to the user

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email



    def set_auth_token(self, token):
        self.auth_token = token
        self.save()

    def set_auth_provider(self, token):
        self.auth_provider = token
        self.save()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Token(models.Model):
    key = models.CharField(max_length=4048)
    user = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)