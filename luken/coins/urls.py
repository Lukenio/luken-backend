from rest_framework.routers import DefaultRouter

from .views import (
    CoinAccountViewSet,
    CreateCoinAccountViewSet
)

coins_router = DefaultRouter()
coins_router.register("coin-accounts", CoinAccountViewSet, base_name="coin-accounts")
coins_router.register("coin-accounts", CreateCoinAccountViewSet, base_name="coin-accounts")
