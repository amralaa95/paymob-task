import logging
from datetime import datetime

from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .custom_permissions import CanUsePromo, IsCanAccess
from .serializers import PromoSerializer
from .models import Promo, DeductPromo
from profiles.models import User

logger = logging.getLogger(__name__)


class PromoResource(viewsets.ModelViewSet):
    permission_classes = (IsCanAccess,)
    parser_classes = (JSONParser,)
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

    def get_queryset(self):
        '''
        - This method will get all promo objects if user is admin role else
          get user's promo objects if user is normal role.
        '''
        if self.request.user.role == User.ADMIN:
            return Promo.objects.all()

        return Promo.objects.filter(user=self.request.user)


class PointResource(viewsets.ModelViewSet):
    permission_classes = (CanUsePromo, )
    parser_classes = (JSONParser, )
    queryset = Promo.objects.all()

    @action(detail=False, methods=['get'], url_path='get_points/(?P<promo_id>\d+)')
    def get_points(self, request, promo_id):
        '''
        - This method will fetch promo object for selected promo id and then get all
          sum of deducted amounts for it and calculate remaining points.
        '''
        try:
            promo_obj = Promo.objects.get(id=promo_id, user=request.user)

            deduct_amount = promo_obj.deductions.all().aggregate(Sum('amount'))
            deduct_amount = deduct_amount.get('amount__sum') if deduct_amount.get('amount__sum') else 0
            remaining_amount = promo_obj.promo_amount - deduct_amount

            return Response({
                'remaining_points': remaining_amount,
                'active': promo_obj.is_active,
                'promo_code': promo_obj.promo_code
            })

        except Promo.DoesNotExist as e:
            logger.exception(f"Error promo code not found")
            return Response({"error": "promo code not found"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(f"Error {e} while use promo code")
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def use_promo(self, request):
        '''
        - This method will make query by selected user, promo is active, start time is less than or equal
          current timeand end time is greater than or equal current time.
        - If promo code is send in request body it'll add to query filter or query will get 
          result by above criteria.
        - If promo code is send and there's query result so it will deduct from this promo object 
          if remaining points greater than or equal amount in request body.
        - Iterate over query result to select promo object that has remaining points greater than or equal
          amount in request body and will deduct from it and stop if promo code is not send in request body.
        - If we can't find any avilable promo from above two steps will raise error message for user.
        '''
        try:
            amount = request.data.get('amount')
            promo_code = request.data.get('promo_code')
            query = {
                'user': request.user,
                'is_active': True,
                'start_time__lte': datetime.now(),
                'end_time__gte': datetime.now(),
            }
            if promo_code:
                query['promo_code'] = promo_code
            if not amount:
                raise APIException('You should enter amount field')

            all_promo_obj = Promo.objects.filter(**query)
            found_promo = False
            for promo_obj in all_promo_obj:
                deduct_amount = promo_obj.deductions.all().aggregate(Sum('amount'))
                deduct_amount = deduct_amount.get('amount__sum') if deduct_amount.get('amount__sum') else 0
                remaining_amount = promo_obj.promo_amount - deduct_amount
                found_promo = remaining_amount >= amount

                if found_promo:
                    DeductPromo.objects.create(promo=promo_obj, amount=amount)
                    logger.info(f"Deducted success from {promo_obj.promo_code}")
                    break
                elif promo_code and not found_promo:
                    logger.error(f"deducted amount is {deduct_amount}, remaining_amount is {remaining_amount}")
                    raise APIException('Amount should be less than or equal remaining amount')

            if promo_code and not found_promo:
                raise APIException('Promo code is not avilable')
            elif not found_promo:
                raise APIException("There's no Promo code is avilable")
            
            return Response({'success': f'Deducted from {promo_obj.promo_code} with amount {amount}'})

        except Promo.DoesNotExist as e:
            logger.exception(f"Error promo code not found")
            return Response({"error": "Promo code not found"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(f"Error {e} while use promo code")
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
