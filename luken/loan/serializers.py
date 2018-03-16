from rest_framework import serializers

from luken.utils.bitcoin_price import get_bitcoin_price

from .models import LoanApplication


class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = "__all__"
        read_only_fields = ("user", "state", "crypto_price_usd")

    def validate(self, attrs):
        user = self.context["request"].user
        user = user if user.is_authenticated else None
        attrs["user"] = user

        email = attrs.get("email")

        if not user and not email:
            raise serializers.ValidationError("email should be specified for unauthenticated users")

        if user and email:
            raise serializers.ValidationError("email should not be specified for authenticated users")

        return attrs

    def create(self, validated_data):
        validated_data["crypto_price_usd"] = get_bitcoin_price()
        return LoanApplication.objects.create(**validated_data)
