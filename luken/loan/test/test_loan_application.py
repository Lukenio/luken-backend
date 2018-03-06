import json

from django.core import mail
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

from ..models import LoanApplication


class BaseLoanApplicationTestCase(TestCase):
    view_name = None

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = G(User)
        self.second_user = G(User)
        self.view_url = reverse_lazy(self.view_name)
        self.view = resolve(self.view_url)


class CreateCoinAccountTestCase(BaseLoanApplicationTestCase):
    view_name = "loan-applications-list"

    def setUp(self):
        super().setUp()

        self.base_loan_application = {
            "loaned_amount": 123.4,
            "crypto_collateral": 1234.5,
            "crypto_price_usd": 10000.0,
            "crypto_type": LoanApplication.TYPES[1][0],
            "terms_month": LoanApplication.TERMS_MONTH_CHOICES[0][0],
        }

        self.test_email = "test@example.com"

        self.invalid_authorized = dict(self.base_loan_application, email=self.test_email)
        self.invalid_unauthorized = dict(self.base_loan_application)

        self.valid_authorized = dict(self.base_loan_application)
        self.valid_unauthorized = dict(self.base_loan_application, email=self.test_email)

    def test_invalid_creation_for_authorized_user(self):
        request = self.factory.post(self.view_url, self.invalid_authorized, format="json")
        force_authenticate(request, user=self.user)
        response = self.view.func(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LoanApplication.objects.count(), 0)

    def test_invalid_creation_for_unauthorized_user(self):
        request = self.factory.post(self.view_url, self.invalid_unauthorized, format="json")
        response = self.view.func(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LoanApplication.objects.count(), 0)

    def test_valid_creation_for_authorized_user(self):
        request = self.factory.post(self.view_url, self.valid_authorized, format="json")
        force_authenticate(request, user=self.user)
        response = self.view.func(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response.render()
        loan_app = json.loads(response.content)

        db_loan_app = LoanApplication.objects.get(pk=loan_app["id"])

        self.assertEqual(db_loan_app.user, self.user)

    def test_valid_creation_for_unauthorized_user(self):
        request = self.factory.post(self.view_url, self.valid_unauthorized, format="json")
        response = self.view.func(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_app = json.loads(response.content)
        db_loan_app = LoanApplication.objects.get(id=loan_app["id"])

        self.assertEqual(db_loan_app.email, self.valid_unauthorized["email"])
        self.assertEqual(len(mail.outbox), 1)

    def test_list_displays_loan_applications_for_current_user_only(self):
        request = self.factory.post(self.view_url, self.valid_authorized, format="json")
        force_authenticate(request, user=self.user)
        self.view.func(request)

        request = self.factory.post(self.view_url, self.valid_authorized, format="json")
        force_authenticate(request, user=self.second_user)
        self.view.func(request)

        request = self.factory.get(self.view_url)
        force_authenticate(request, user=self.user)
        response = self.view.func(request)
        response.render()

        second_user_loan_app_ids = LoanApplication.objects\
            .filter(user=self.second_user)\
            .values_list("pk", flat=True)

        first_user_loan_apps = json.loads(response.content)
        self.assertGreater(len(first_user_loan_apps["results"]), 0)
        for app in first_user_loan_apps["results"]:
            self.assertTrue(app["id"] not in second_user_loan_app_ids)
