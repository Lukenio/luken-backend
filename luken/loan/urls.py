from rest_framework.routers import SimpleRouter

from .views import (
    LoanApplicationViewSet,
    CreateLoanApplicationViewSet,
)

loan_router = SimpleRouter()
loan_router.register("loan-applications", LoanApplicationViewSet, base_name="loan-applications")
loan_router.register("loan-applications", CreateLoanApplicationViewSet, base_name="loan-applications")
