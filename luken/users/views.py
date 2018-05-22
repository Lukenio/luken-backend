import logging
import json
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, KYC
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, KYCSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest
from pusher import Pusher


logger = logging.getLogger(__name__)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrives user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

class KYCApiView(generics.ListCreateAPIView): 
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return KYC.objects.filter(user=self.request.user)

class KYCApiRetrieveView(generics.RetrieveUpdateDestroyAPIView): 
    lookup_field = 'pk'
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return KYC.objects.filter(user=self.request.user)