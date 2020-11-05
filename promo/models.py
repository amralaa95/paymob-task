import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from profiles.models import User
from core.models import TimeStampedModel


def generate_promo_code():
    return str(uuid.uuid4()).replace('-', '')


class Promo(TimeStampedModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="promos")
    promo_type = models.CharField(max_length=50)
    promo_code = models.CharField(max_length=40, unique=True, default=generate_promo_code)
    promo_amount = models.IntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=300)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)


class DeductPromo(TimeStampedModel, models.Model):
    '''
    - Make this model to store deducted actions for each promo and not store calculated value in field
      in Promo table to be able extend deduction operation to add more details for it for the future.
    '''
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE, related_name="deductions")
    amount = models.IntegerField()
