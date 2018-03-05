from rest_framework.routers import SimpleRouter

from .views import LoanApplicationViewSet

loan_router = SimpleRouter()
loan_router.register("loan-applications", LoanApplicationViewSet, base_name="loan-applications")
