from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from core.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    '''
    - Extend django default User model and add some attributes to differentiate between
      Admin user and Normal user. 
    '''
    ADMIN = 'ADMIN'
    NORMAL = 'NORMAL'

    PROFILE_CHOICES = (
        (ADMIN, ADMIN),
        (NORMAL, NORMAL),
    )

    role = models.CharField(max_length=30, choices=PROFILE_CHOICES)
    phone_number = PhoneNumberField(null=True, blank=True)
