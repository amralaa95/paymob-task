import logging

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import JSONParser

from .serializers import UserSerializer
from profiles.models import User


logger = logging.getLogger(__name__)


class UserResource(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    parser_classes = (JSONParser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
