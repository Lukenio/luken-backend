from django.contrib import admin

from .models import WalletAddress


@admin.register(WalletAddress)
class WalletAddressAdmin(admin.ModelAdmin):
    pass
