from rest_framework import serializers
from django.db.models import Sum
from .models import Promo, DeductPromo
from profiles.models import User
from rest_framework.exceptions import NotAcceptable


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'
        read_only_fields = ['promo_code', 'created', 'modified']

    def validate(self, data):
        '''
        - This method works when user add/update promo object to validate:
          - if user is admin so it will raise errorr .
          - if start_time is greater than end_time so it will raise error.
        '''
        if data.get('user') and data.get('user').role == User.ADMIN:
            raise NotAcceptable("Can't assign promo code for admin user")

        if data.get('end_time') and data.get('start_time') and data.get('end_time') < data.get('start_time'):
            raise NotAcceptable("Start time should be before end time")

        return data

    def update(self, promo_obj, validated_data):
        '''
        - This method works when user update promo object to validate:
          - if user is use this promo code so can't thange user to another user.
          - if new amount is less than deducted amount.
        '''
        deduct_amount = DeductPromo.objects.filter(promo=promo_obj).aggregate(Sum('amount'))
        if validated_data.get('user') and validated_data.get('user') != promo_obj.user and deduct_amount.get(
                'amount__sum'):
            raise NotAcceptable(f"Can't change the user, this promo was used.")

        if deduct_amount.get('amount__sum') and validated_data.get('promo_amount') and \
           deduct_amount.get('amount__sum') > validated_data.get('promo_amount'):
            raise NotAcceptable(
                f"Promo amount should be greater than deducted amount {deduct_amount.get('amount__sum')}")

        super().update(promo_obj, validated_data)
        return promo_obj
