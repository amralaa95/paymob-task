import factory
from factory.django import DjangoModelFactory

from .models import Promo


class PromoFactory(DjangoModelFactory):
    class Meta:
        model = Promo

    promo_type = 'test'
    description = 'test'
    promo_amount = factory.Faker('promo_amount')
    start_time = factory.Faker('start_time')
    end_time = factory.Faker('end_time')
    is_active = True
