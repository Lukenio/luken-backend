from rest_framework import (
    viewsets,
)
from rest_framework.permissions import IsAuthenticated

from luken.utils.views import PermissionByActionMixin

from .models import CoinAccount
from .permissions import OwnerOnly
from .serializers import CoinAccountSerializer


class CoinAccountViewSet(PermissionByActionMixin, viewsets.ModelViewSet):
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "default": [OwnerOnly],
    }
    """
    CRUD operations for Coin Accounts.
    """
    queryset = CoinAccount.objects.all()
    serializer_class = CoinAccountSerializer
