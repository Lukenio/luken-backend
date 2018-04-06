from django.contrib import admin

from .models import (
    CoinAccount,
    Transaction
)


class TransactionInline(admin.TabularInline):
    model = Transaction


@admin.register(CoinAccount)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]
