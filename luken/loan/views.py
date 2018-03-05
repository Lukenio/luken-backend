from rest_framework import (
    viewsets,
    permissions,
)

from luken.coins.permissions import OwnerOnly
from luken.utils.views import PermissionByActionMixin

from .models import LoanApplication
from .serializers import LoanApplicationSerializer


class LoanApplicationViewSet(PermissionByActionMixin, viewsets.ModelViewSet):
    """
    RUD operations for Loan Applications.
    """
    permission_classes_by_action = {
        "create": [permissions.AllowAny],
        "default": [OwnerOnly],
    }
    serializer_class = LoanApplicationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.loan_applications.all()
        else:
            return LoanApplication.objects.none()
