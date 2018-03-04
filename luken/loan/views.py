from rest_framework import (
    viewsets,
    mixins,
    permissions,
)

from luken.coins.permissions import OwnerOnly

from .models import LoanApplication
from .serializers import (
    LoanApplicationSerializer,
    CreateLoanApplicationSerializer
)


class LoanApplicationViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    RUD operations for Loan Applications.
    """
    permission_classes = (permissions.IsAuthenticated, OwnerOnly, )
    serializer_class = LoanApplicationSerializer

    def get_queryset(self):
        return LoanApplication.objects.filter(user=self.request.user)


class CreateLoanApplicationViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Create op for Loan Applications.
    """
    queryset = LoanApplication.objects.all()
    serializer_class = CreateLoanApplicationSerializer
    permission_classes = (permissions.AllowAny, )
