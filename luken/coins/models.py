from django.conf import settings
from django.db import models


class CoinAccount(models.Model):
    TYPES = (
        (0, "Bitcoin"),
        (1, "Bitcoin Cache"),
        (2, "Lite Coin"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coin_accounts")
    name = models.CharField(max_length=127)
    type = models.IntegerField(choices=TYPES)
    pub_address = models.CharField(max_length=255)
    vault_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.name} - {self.get_type_display()}"
