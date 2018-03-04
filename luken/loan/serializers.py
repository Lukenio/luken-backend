from rest_framework import serializers

from .models import LoanApplication


class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = "__all__"
        read_only_fields = ("user", "state", "bitcoin_price_usd", )


class CreateLoanApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta(LoanApplicationSerializer.Meta):
        read_only_fields = ()

    def validate(self, attrs):
        if not attrs["user"] and not attrs["email"]:
            raise serializers.ValidationError("email should be specified for unauthenticated users")

        if attrs["user"] and attrs["email"]:
            raise serializers.ValidationError("email should not be specified for authenticated users")

        return attrs
