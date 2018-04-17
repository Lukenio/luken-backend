from django.conf import settings
from django.db import models
from django.db.models import Sum

from .services import (
    get_coin_backend,
    BITCOIN_TYPE,
    ETHEREUM_TYPE,
)


class CoinAccount(models.Model):

    TYPES = (
        (0, BITCOIN_TYPE),
        (1, ETHEREUM_TYPE),
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

    @classmethod
    def assign_default_accounts_to_new_user(cls, sender, instance, created, **kwargs):
        if not created:
            return

        for coin_account_type in cls.TYPES:
            db_type, description = coin_account_type

            cls.objects.create(
                user=instance,
                name=f"Default {description} account",
                type=db_type,
            )

    @classmethod
    def assign_pub_address(cls, sender, instance, created, **kwargs):
        if not created:
            return

        type_display = instance.get_type_display()
        coin_backend = get_coin_backend(type_display)
        instance.pub_address = coin_backend.get_address(instance.id)
        instance.save()

    def balance(self):
        received_amount = self.transactions\
            .filter(type=Transaction.RECEIVED)\
            .aggregate(Sum('amount'))

        sent_amount = self.transactions\
            .filter(type=Transaction.SENT)\
            .aggregate(Sum('amount'))

        return (received_amount['amount__sum'] or 0) - (sent_amount['amount__sum'] or 0)


class Transaction(models.Model):

    RECEIVED = 0
    SENT = 1

    TYPES = (
        (RECEIVED, "Received"),
        (SENT, "Sent"),
    )

    account = models.ForeignKey(CoinAccount, on_delete=models.PROTECT, related_name="transactions")
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.SmallIntegerField(choices=TYPES)
    address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    value_usd = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.get_type_display()} transaction on {self.account} at {self.datetime}"


class WithdrawRequest(models.Model):
    account = models.ForeignKey(CoinAccount, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    updated = models.DateTimeField(auto_now=True)
    pub_address = models.CharField(max_length=255)


models.signals.post_save.connect(
    CoinAccount.assign_default_accounts_to_new_user,
    sender=settings.AUTH_USER_MODEL
)
models.signals.post_save.connect(CoinAccount.assign_pub_address, sender=CoinAccount)
