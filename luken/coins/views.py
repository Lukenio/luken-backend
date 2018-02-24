from rest_framework import (
    viewsets,
    mixins,
)

from .models import CoinAccount
from .permissions import OwnerOnly
from .serializers import CoinAccountSerializer


class CoinAccountViewSet(
    mixins.CreateModelMixin,
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
