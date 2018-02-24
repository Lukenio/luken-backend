from django.contrib import admin

from .models import CoinAccount


@admin.register(CoinAccount)
class UserAdmin(admin.ModelAdmin):
    pass
