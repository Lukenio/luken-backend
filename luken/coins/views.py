from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.permissions import AllowAny

from .models import CoinAccount
from .permissions import OwnerOnly
from .serializers import CoinAccountSerializer


class CoinAccountViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    CRUD operations for Coin Accounts.
    """
    queryset = CoinAccount.objects.all()
    serializer_class = CoinAccountSerializer
    permission_classes = (OwnerOnly, )


class CreateCoinAccountViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CoinAccount.objects.all()
    serializer_class = CoinAccountSerializer
    permission_classes = (AllowAny, )
