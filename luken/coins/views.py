from django.conf import settings

from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.status import HTTP_200_OK

from luken.utils.views import PermissionByActionMixin

from .models import (
    CoinAccount,
    Transaction
)
from .permissions import OwnerOnly
from .serializers import CoinAccountSerializer, WithdrawRequestSerializer


class ModelCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
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

    @action(methods=['post'], detail=True)
    def withdraw_request(self, request, pk=None):
        data = dict(request.data)
        data["account"] = pk
        serializer = WithdrawRequestSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(request.data)

    @action(methods=["get", "post"], detail=True)
    def process_transaction(self, request, pk):
        if request.GET.get("secret") != settings.BLOCKCHAIN_CALLBACK_SECRET:
            raise ParseError()

        try:
            value_in_satoshi = int(request.GET["value"])
        except (KeyError, ValueError):
            raise ParseError("bad or missing value")

        value_in_btc = value_in_satoshi / 100000000

        account = get_object_or_404(CoinAccount.objects.all(), pk=pk)

        Transaction.objects.create(account=account, type=Transaction.RECEIVED, amount=value_in_btc)

        return Response(status=HTTP_200_OK)
