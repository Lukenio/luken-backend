from rest_framework.routers import SimpleRouter

from .views import CoinAccountViewSet

coins_router = SimpleRouter()
coins_router.register("coin-accounts", CoinAccountViewSet, base_name="coin-accounts")
