from django.db import models    
from django.urls import reverse
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import slugify
import secrets
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import random

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    plan_choices =[
        ('trial','trial'),
        ('subscriber', 'subscriber'),
        ('developer','developer')
    ]
    """
    Default custom user model for chatrep2.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(null=False, unique=True)
    request_count=models.IntegerField(default=0)
    email_confirmed = models.BooleanField(default=False)
    reset_password = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.email.split('@')[0]+ str(random.randint(1, 10000)))
        return super().save(*args, **kwargs)
    
