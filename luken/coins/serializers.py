from rest_framework import serializers

from .models import CoinAccount


class CoinAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoinAccount
        fields = "__all__"
        read_only_fields = ("created", "updated", "user", )
