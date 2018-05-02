from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
from luken.coins.serializers import CoinAccountSerializer

from rest_registration.api.serializers import _get_field_names


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)
        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'email', 'auth_token', 'kyc_applied')
        read_only_fields = ('auth_token', 'kyc_applied')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):

    coin_accounts = CoinAccountSerializer(many=True)
    kyc = serializers.JSONField(source='get_kyc', read_only=True)

    def __init__(self, *args, **kwargs):
        user_class = get_user_model()
        field_names = _get_field_names(allow_primary_key=True)
        read_only_field_names = _get_field_names(allow_primary_key=True,
                                                 non_editable=True)

        field_names += ('coin_accounts', 'kyc')
        read_only_field_names += ('coin_accounts', 'kyc')

        class MetaObj(object):
            pass

        self.Meta = MetaObj()
        self.Meta.model = user_class
        self.Meta.fields = field_names
        self.Meta.read_only_fields = read_only_field_names

        super().__init__(*args, **kwargs)
