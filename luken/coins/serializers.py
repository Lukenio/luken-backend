from rest_framework import serializers

from .models import CoinAccount


class CoinAccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = CoinAccount
        fields = "__all__"
        read_only_fields = ("created", "updated", "user", "vault_id", "pub_address")
