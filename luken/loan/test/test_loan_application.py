import json

from django.core import mail
from django.test import TestCase, override_settings
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
from luken.partners.models import Partner

from ..models import LoanApplication


@override_settings(COIN_BACKENDS={
    "Bitcoin": "luken.coins.test.TestBackend",
    "Ethereum": "luken.coins.test.TestBackend"
})
class BaseLoanApplicationTestCase(TestCase):
    view_name = None

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = G(User)
        self.second_user = G(User)
        self.view_url = reverse_lazy(self.view_name)
        self.view = resolve(self.view_url)


class CreateLoanApplicationTestCase(BaseLoanApplicationTestCase):
    view_name = "loan-applications-list"

    def setUp(self):
        super().setUp()

        self.base_loan_application = {
            "loaned_amount": 3000.4,
            "total_loaned_amount": 3500.0,
            "ltv": 0.35,
            "apr": 0.2,
            "crypto_collateral": 1234.5,
            "crypto_price_usd": 10000.0,
            "terms_of_service_agree": True,
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

    def test_anon_loan_connection_to_newly_created_user(self):
        request = self.factory.post(self.view_url, self.valid_unauthorized, format="json")
        response = self.view.func(request)
        response.render()

        loan_app = json.loads(response.content)
        loan_app = LoanApplication.objects.get(id=loan_app["id"])

        bound_user = G(User, email=loan_app.email)
        loan_app.refresh_from_db()
        self.assertEqual(loan_app.user, bound_user)

    def test_creates_new_user_account_when_approved(self):
        request = self.factory.post(self.view_url, self.valid_unauthorized, format="json")
        response = self.view.func(request)

        response.render()
        loan_app = json.loads(response.content)
        loan_app = LoanApplication.objects.get(id=loan_app["id"])

        loan_app.state = loan_app.APPROVED_STATE
        loan_app.save()

        User.objects.get(email=loan_app.email)

    def test_sends_email_for_unauthorized(self):
        request = self.factory.post(self.view_url, self.valid_unauthorized, format="json")
        response = self.view.func(request)

        response.render()
        loan_app = json.loads(response.content)
        loan_app = LoanApplication.objects.get(id=loan_app["id"])

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("Loan Application" in mail.outbox[0].body)
        mail.outbox.clear()

        loan_app.state = loan_app.APPROVED_STATE
        loan_app.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(loan_app.get_crypto_type_display() in mail.outbox[0].body)
        self.assertTrue(loan_app.email in mail.outbox[0].body)
        pub_address = loan_app.user.coin_accounts.get(type=loan_app.crypto_type).pub_address
        self.assertTrue(pub_address in mail.outbox[0].body)
        mail.outbox.clear()

        loan_app.state = loan_app.DECLINED_STATE
        loan_app.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("Declined" in mail.outbox[0].body)
        mail.outbox.clear()

    def test_sends_email_for_authorized(self):
        request = self.factory.post(self.view_url, self.valid_authorized, format="json")
        force_authenticate(request, user=self.user)
        response = self.view.func(request)

        response.render()
        loan_app = json.loads(response.content)
        loan_app = LoanApplication.objects.get(id=loan_app["id"])

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("Loan Application" in mail.outbox[0].body)
        mail.outbox.clear()

        loan_app.state = loan_app.APPROVED_STATE
        loan_app.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(loan_app.get_crypto_type_display() in mail.outbox[0].body)
        self.assertTrue(loan_app.user.email in mail.outbox[0].body)
        pub_address = loan_app.user.coin_accounts.get(type=loan_app.crypto_type).pub_address
        self.assertTrue(pub_address in mail.outbox[0].body)
        mail.outbox.clear()

        loan_app.state = loan_app.DECLINED_STATE
        loan_app.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("Declined" in mail.outbox[0].body)
        mail.outbox.clear()

    def test_assign_partner_if_token_provided(self):
        partner = G(Partner)
        token = partner.tokens.first().id
        loan_app_request = dict(self.valid_unauthorized, partner_token=token)

        request = self.factory.post(self.view_url, loan_app_request, format="json")
        response = self.view.func(request)

        response.render()
        loan_app = json.loads(response.content)
        loan_app = LoanApplication.objects.get(id=loan_app["id"])

        self.assertEqual(loan_app.partner, partner)
