import json

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

from ..models import (
    CoinAccount,
    Transaction,
    WithdrawRequest
)


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

    def test_withdraw_request(self):
        withdraw_amount = 0.1

        request_data = {
            "amount": withdraw_amount,
            "pub_address": "hellowoeld"
        }

        acc = G(CoinAccount)
        G(Transaction, account=acc, type=Transaction.RECEIVED, amount=withdraw_amount + 1)

        url = reverse_lazy('coin-accounts-withdraw-request', args=[acc.id])
        view = resolve(url)
        request = self.factory.post(url, request_data, format="json")
        response = view.func(request, pk=acc.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)

    def test_error_if_withdrawal_amount_is_greater_than_account_amount(self):
        withdraw_amount = 2.1

        request_data = {
            "amount": withdraw_amount,
            "pub_address": "hello-world"
        }

        acc = G(CoinAccount)
        G(Transaction, account=acc, type=Transaction.RECEIVED, amount=withdraw_amount - 1)

        url = reverse_lazy('coin-accounts-withdraw-request', args=[acc.id])
        view = resolve(url)
        request = self.factory.post(url, request_data, format="json")
        response = view.func(request, pk=acc.id)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)

    def test_returns_pending_withdrawal_amount(self):
        account = G(CoinAccount, user=self.user)
        withdraw_request = G(WithdrawRequest, account=account)

        url = reverse_lazy('coin-accounts-detail', args=[account.id])
        view = resolve(url)

        request = self.factory.get(url, format="json")
        force_authenticate(request, user=self.user)
        response = view.func(request, pk=account.id)
        response.render()

        account_from_response = json.loads(response.content)

        self.assertEqual(account_from_response["pending_withdrawal_request"], withdraw_request.amount)
