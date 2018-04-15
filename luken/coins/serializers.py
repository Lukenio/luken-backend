from rest_framework import serializers

from .models import CoinAccount, WithdrawRequest


class CoinAccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    balance = serializers.ReadOnlyField()
    pending_withdrawal_request = serializers.ReadOnlyField(source='pending_withdrawal_amount')

    class Meta:
        model = CoinAccount
        fields = "__all__"
        read_only_fields = ("created", "updated", "user", "vault_id", "pub_address", "balance")


class WithdrawRequestSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=CoinAccount.objects.all())

    class Meta:
        model = WithdrawRequest
        fields = "__all__"
        read_only_fields = ("created", "updated")

    def validate(self, attrs):
        account = attrs["account"]
        amount = attrs["amount"]

        if account.balance() - account.pending_withdrawal_amount < amount:
            raise serializers.ValidationError("insufficient funds on account")

        return attrs
