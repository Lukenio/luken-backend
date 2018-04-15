from django.contrib import admin

from luken.utils.admin import ReadonlyTabularInline

from .models import (
    Partner,
    PartnerToken
)


class PartnerTokenInline(ReadonlyTabularInline):
    model = PartnerToken


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    inlines = [
        PartnerTokenInline,
    ]
