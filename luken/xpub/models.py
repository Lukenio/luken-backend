from django.db import models


class WalletAddress(models.Model):
    NETWORKS = (
        (0, "BTC"),
        (1, "ETH"),
        (2, "LTC"),
    )

    type = models.SmallIntegerField(choices=NETWORKS)
    address = models.CharField(max_length=63)
    xpub = models.CharField(max_length=255)
    derivation_path = models.CharField(max_length=31)
    child = models.IntegerField()

    def __str__(self):
        return f"{self.type} - {self.address}"
