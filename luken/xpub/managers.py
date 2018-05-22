from django.conf import settings
from django.db import models

from pywallet import wallet


class WalletAddressManager(models.Manager):

    def generate(self, network, tracking_id):
        response = wallet.create_address(network, settings.BLOCKCHAIN_XPUB, tracking_id)
        self.create(
            type=network,
            address=response["address"],
            xpub=settings.BLOCKCHAIN_XPUB,
            derivation_path=response["path"],
            child=tracking_id
        )
