from rest_framework import serializers

from .models import LoanApplication


class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = "__all__"
        read_only_fields = ("user", "state", "bitcoin_price_usd", )

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
        validated_data["bitcoin_price_usd"] = 6000.0
        return LoanApplication.objects.create(**validated_data)
