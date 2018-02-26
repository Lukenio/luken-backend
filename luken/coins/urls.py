from rest_framework.routers import SimpleRouter

from .views import (
    CoinAccountViewSet,
    CreateCoinAccountViewSet
)

coins_router = SimpleRouter()
coins_router.register("coin-accounts", CoinAccountViewSet, base_name="coin-accounts")
coins_router.register("coin-accounts", CreateCoinAccountViewSet, base_name="coin-accounts")
