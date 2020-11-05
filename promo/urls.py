from rest_framework import routers
from .views import PromoResource, PointResource

promo_router = routers.SimpleRouter()
promo_router.register(r'promos', PromoResource)
promo_router.register(r'points', PointResource)
