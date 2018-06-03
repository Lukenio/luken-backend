from dateutil.relativedelta import relativedelta
import calendar

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import loader
from django.core.mail import send_mail

import reversion
from django.utils import timezone
from reversion.models import Version

from luken.utils.random import generate_random_string
from luken.utils.hello_sign import client


@reversion.register()
class LoanApplication(models.Model):
    ONE_MONTH = 1
    THREE_MONTH = 3
    SIX_MONTH = 6
    TWELVE_MONTH = 12

    TERMS_MONTH_CHOICES = (
        (ONE_MONTH, "1 Month"),
        (THREE_MONTH, "3 Month"),
        (SIX_MONTH, "6 Month"),
        (TWELVE_MONTH, "12 Month"),
    )

    BITCOIN_TYPE = 0
    ETHEREUM_TYPE = 1
    TYPES = (
        (BITCOIN_TYPE, "Bitcoin"),
        (ETHEREUM_TYPE, "Etherium"),
    )

    SUBMITTED_STATE = 0
    IN_REVIEW_STATE = 1
    APPROVED_STATE = 2
    DECLINED_STATE = 3
    FUNDED_STATE = 4
    RELEASED_STATE = 5
    KYC_SUBMITTED = 6
    KYC_VERIFIED = 7
    CONTRACT_SIGNED = 8

    STATE_CHOICES = (
        (SUBMITTED_STATE, "Submitted"),
        (IN_REVIEW_STATE, "In Review"),
        (APPROVED_STATE, "Approved"),
        (DECLINED_STATE, "Declined"),
        (KYC_SUBMITTED, "KYC Submitted"),
        (KYC_VERIFIED, "KYC Verified"),
        (CONTRACT_SIGNED, "Contract Signed"),
        (FUNDED_STATE, "Funded"),
        (RELEASED_STATE, "Loan released"),
    )

    EMAIL_TEMPLATES = {
        SUBMITTED_STATE: (
            loader.get_template("loan/on_submit.txt"),
            loader.get_template("loan/on_submit.html"),
        ),
        APPROVED_STATE: (
            loader.get_template("loan/on_approval.txt"),
            loader.get_template("loan/on_approval.html"),
        ),
        DECLINED_STATE: (
            loader.get_template("loan/on_decline.txt"),
            loader.get_template("loan/on_decline.html"),
        ),
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="loan_applications",
        on_delete=models.PROTECT, null=True
    )
    email = models.EmailField(blank=True)
    partner = models.ForeignKey(
        "partners.Partner", related_name="loan_applications",
        on_delete=models.PROTECT, null=True
    )
    loaned_amount = models.DecimalField(decimal_places=2, max_digits=20)
    crypto_collateral = models.DecimalField(decimal_places=8, max_digits=20)
    crypto_price_usd = models.DecimalField(decimal_places=2, max_digits=20)
    crypto_type = models.SmallIntegerField(choices=TYPES)
    terms_month = models.SmallIntegerField(choices=TERMS_MONTH_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=STATE_CHOICES[0][0])
    terms_of_service_agree = models.BooleanField()
    total_loaned_amount = models.DecimalField(decimal_places=2, max_digits=20)
    ltv = models.DecimalField(decimal_places=2, max_digits=4)
    apr = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return f"Loan Application - {self.user or self.email}"

    @classmethod
    def post_save_dispatch(cls, sender, instance, created, **kwargs):
        if created:
            instance.send_email()

            # if user exists than attach loan to user right away
            user_class = get_user_model()
            try:
                user = user_class.objects.get(email=instance.email)
                instance.user = user
                instance.save()
            finally:
                return

        latest = instance.get_latest_revision()
        if instance.state <= latest.field_dict["state"]:
            return

        if instance.state == cls.APPROVED_STATE:
            instance.on_approval()
        elif instance.state == cls.DECLINED_STATE:
            instance.on_decline()

    def send_email(self, **ctx):
        ctx["loan"] = self

        text_template, html_template = self.EMAIL_TEMPLATES[self.state]
        text_content = text_template.render(ctx)
        html_content = html_template.render(ctx)

        email = self.get_borrower_email()

        msg = EmailMultiAlternatives(
            "Crypto Loan Application",
            text_content,
            "apply@loanz.io",
            [email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def on_approval(self):
        if self.user is None:
            password = self.create_user_account_after_approval()
            self.refresh_from_db()

            self.send_email(
                address=self.user.coin_accounts.get(type=self.crypto_type).pub_address,
                password=password
            )

    def on_decline(self):
        self.send_email()

    def create_user_account_after_approval(self):
        assert self.user is None

        if self.state == self.APPROVED_STATE:
            password = generate_random_string(length=8)
            get_user_model().objects.create_user(
                username=self.email,
                email=self.email,
                password=password,
            )
        return password

    @classmethod
    def notify_when_user_created(cls, sender, instance, created, **kwargs):

        if not created:
            return

        send_mail(
            "A new user created",
            "A new user created with email: {}".format(instance.email),
            'newuser@loanz.io',
            ['apply@loanz.io', ],
            fail_silently=True,
        )

    @classmethod
    def connect_to_user_after_creation(cls, sender, instance, created, **kwargs):
        if not created:
            return

        cls.objects.filter(user=None, email=instance.email).update(user=instance)

    def get_latest_revision(self):
        try:
            return Version.objects.get_for_object(self).latest("revision__date_created")
        except Version.DoesNotExist:
            return None

    def get_approval_prob_percent(self):
        return self.apr * 100

    def get_maturity_date(self):
        return self.created + relativedelta(months=self.terms_month)

    def get_borrower_email(self):
        return self.email or self.user.email

    def sign_contract_with_hello_sign(self):
        template_id = "0558d2f6c9f02acf7f16422f69582ff72cb810f7"
        fee = "3%"

        now = timezone.now()
        _admin_name, admin_email = settings.ADMINS[0]
        lender_name = "Emedel Holding Inc."

        client.send_signature_request_with_template(
            test_mode=True,
            template_id=template_id,
            title="LOANZ Loan Agreement",
            subject="LOANZ Loan Agreement",
            message="Please sign this Loan Agreement. Let me know if you have any questions.",
            signers=[
                {"role_name": "Borrower", "email_address": self.get_borrower_email(), "name": "?"},
                {"role_name": "Lender", "email_address": admin_email, "name": lender_name}
            ],
            custom_fields=[
                {"borrower_name": self.user.get_full_name() if self.user else ""},
                {"principal_amount": self.loaned_amount},
                # not sure if I am right to use `apr` here
                {"interest_rate": self.apr},
                {"term_of_loan": self.get_terms_month_display()},
                {"commencement_date": now},
                {"maturity_date": self.get_maturity_date()},
                {"type_of_crypto": self.get_crypto_type_display()},
                {"amount_of_crypto": self.crypto_collateral},
                {"value_of_crypto": self.crypto_price_usd},
                {"lenders_fee_apr": self.apr},
                {"loanz_fee": fee},
                {"legal_cost": 0},
                {"net_advance": self.loaned_amount},
                {"day": now.day},
                {"month_text": calendar.month_name[now.month]},
                {"year_2_numbers": now.strftime("%y")},
                {"loan_amount": self.loaned_amount},
                {"landing_currency": "USD"},
                {"principal_interest_text": self.apr},
                {"borrower_email": self.get_borrower_email()},
                {"loanz_email": admin_email},
                {"lender_email": admin_email},
                {"lender_name": lender_name}
            ]
        )


models.signals.post_save.connect(LoanApplication.post_save_dispatch, sender=LoanApplication)
models.signals.post_save.connect(
    LoanApplication.connect_to_user_after_creation,
    sender=settings.AUTH_USER_MODEL
)

models.signals.post_save.connect(
    LoanApplication.notify_when_user_created,
    sender=settings.AUTH_USER_MODEL
)
