from django.contrib import admin

from luken.utils.admin import ReadonlyTabularInline

from .models import (
    CoinAccount,
    Transaction
)


class TransactionInline(ReadonlyTabularInline):
    model = Transaction


@admin.register(CoinAccount)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]
