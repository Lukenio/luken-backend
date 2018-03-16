from django.conf import settings
from django.db import models

from .services import get_coin_backend


class CoinAccount(models.Model):
    TYPES = (
        (0, "Bitcoin"),
        (1, "Etherium"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coin_accounts")
    name = models.CharField(max_length=127)
    type = models.IntegerField(choices=TYPES)
    pub_address = models.CharField(max_length=255)
    vault_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.name} - {self.get_type_display()}"

    def save(self, *args, **kwargs):
        if not self.pk:
            type_display = self.get_type_display()

            coin_bakend = get_coin_backend(type_display.lower().replace(" ", ""))

            self.pub_address = coin_bakend().get_address(self.user.id)

        super().save(*args, **kwargs)


class Transaction(models.Model):
    TYPES = (
        (0, "Received"),
        (1, "Sent"),
    )

    account = models.ForeignKey(CoinAccount, on_delete=models.PROTECT, related_name="transactions")
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.SmallIntegerField(choices=TYPES)
    address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    value_usd = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.get_type_display()} transaction on {self.account} at {self.datetime}"
