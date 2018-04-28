from rest_framework import serializers
from rest_framework.exceptions import NotFound

from luken.utils.bitcoin_price import get_bitcoin_price

from luken.partners.models import PartnerToken

from .models import LoanApplication


class LoanApplicationSerializer(serializers.ModelSerializer):

    loaned_amount = serializers.DecimalField(decimal_places=2,
                                             max_digits=20,
                                             max_value=1000000.00,
                                             min_value=500)

    ltv = serializers.DecimalField(decimal_places=2,
                                   max_digits=3,
                                   max_value=1.0,
                                   min_value=0.1)

    apr = serializers.DecimalField(decimal_places=2,
                                   max_digits=3,
                                   max_value=1.0,
                                   min_value=0.1)

    partner_token = serializers.UUIDField(required=False)

    maturity_date = serializers.DateTimeField(source='get_maturity_date',
                                              read_only=True)

    class Meta:
        model = LoanApplication
        fields = "__all__"
        read_only_fields = ("user", "state", "crypto_price_usd", "maturity_date")

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

        partner_token = validated_data.pop("partner_token", None)
        if partner_token:
            try:
                partner = PartnerToken.objects.get(pk=partner_token).partner
                validated_data["partner"] = partner
            except PartnerToken.DoesNotExist:
                raise NotFound(detail="provided partner token is not found")

        return LoanApplication.objects.create(**validated_data)
