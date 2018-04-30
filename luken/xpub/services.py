from django.conf import settings
from django.urls import reverse

from luken.utils.txhash import create_tracker
from luken.utils.url import update_url_query_params

from .models import WalletAddress


class WalletAddressBackendBase(object):
    coin_type = None

    def get_pubkey(self):
        pass

    def create_wallet(self):
        pass

    def get_address(self, tracking_id):
        wallet_address = WalletAddress.objects.generate(self.coin_type, tracking_id)
        callback_url = settings.HOST_URL + reverse("transaction-received-webhook")
        callback_url = update_url_query_params(
            callback_url,
            sender="$sender",
            address="$address",
            amount="$amount",
            txhash="$txhash"
        )
        create_tracker(
            wallet_address.child, wallet_address.type,
            wallet_address.address, callback_url
        )


class BitcoinAddressBackend(WalletAddressBackendBase):
    coin_type = "BTC"


class EthereumAddressBackend(WalletAddressBackendBase):
    coin_type = "ETH"


class LiteCoinAddressBackend(WalletAddressBackendBase):
    coin_type = "LTC"
