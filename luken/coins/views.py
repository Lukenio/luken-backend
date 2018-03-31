from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.response import Response


from luken.utils.views import PermissionByActionMixin

from .models import CoinAccount, WithdrawRequest
from .permissions import OwnerOnly
from .serializers import CoinAccountSerializer, WithdrawRequestSerializer


class ModelCreateViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `create()` action
    """
    pass


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

    @detail_route(methods=['post'])
    def withdraw_request(self, request, pk=None):
        data = dict(request.data)
        data["account"] = pk
        serializer = WithdrawRequestSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(request.data)
