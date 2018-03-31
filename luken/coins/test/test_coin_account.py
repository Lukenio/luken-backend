from decimal import Decimal
from django.test import TestCase
from django.urls import (
    reverse_lazy,
    resolve,
)
from django_dynamic_fixture import G
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
    force_authenticate
)

from luken.users.models import User

from ..models import CoinAccount, Transaction


class BaseCoinAccountTestCase(TestCase):
    view_name = None

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = G(User)
        self.view_url = reverse_lazy(self.view_name)
        self.view = resolve(self.view_url)


class CreateCoinAccountTestCase(BaseCoinAccountTestCase):
    view_name = "coin-accounts-list"

    def setUp(self):
        super().setUp()
        self.valid_coin_account = {
            "name": "test",
            "type": CoinAccount.TYPES[0][0],
            "pub_address": "test",
            "vault_id": "test",
        }

    def test_valid_creation(self):
        request = self.factory.post(self.view_url, self.valid_coin_account, format="json")
        force_authenticate(request, user=self.user)
        response = self.view.func(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content)

    def test_default_accounts_creation(self):
        new_user = G(User)

        self.assertEqual(CoinAccount.objects.filter(user=new_user).count(), len(CoinAccount.TYPES))

    def test_balance_field(self):

        acc = G(CoinAccount)
        G(Transaction, amount=Decimal('4.201'),
          type=Transaction.RECEIVED, account=acc)
        G(Transaction, amount=Decimal('3.1'),
          type=Transaction.SENT, account=acc)

        self.assertEquals(acc.balance(), Decimal('4.201') - Decimal('3.1'))
