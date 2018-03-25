from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import loader

import reversion
from reversion.models import Version

from luken.utils.random import generate_random_string


@reversion.register()
class LoanApplication(models.Model):
    TERMS_MONTH_CHOICES = (
        (0, "3 Month"),
        (1, "6 Month"),
        (2, "12 Month"),
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
    STATE_CHOICES = (
        (SUBMITTED_STATE, "Submitted"),
        (IN_REVIEW_STATE, "In Review"),
        (APPROVED_STATE, "Approved"),
        (DECLINED_STATE, "Declined"),
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
    loaned_amount = models.DecimalField(decimal_places=2, max_digits=20)
    crypto_collateral = models.DecimalField(decimal_places=8, max_digits=20)
    crypto_price_usd = models.DecimalField(decimal_places=2, max_digits=20)
    crypto_type = models.SmallIntegerField(choices=TYPES)
    terms_month = models.SmallIntegerField(choices=TERMS_MONTH_CHOICES)
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=STATE_CHOICES[0][0])

    total_loaned_amount = models.DecimalField(decimal_places=2, max_digits=20)
    ltv = models.DecimalField(decimal_places=2, max_digits=4)
    apr = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return f"Loan Application - {self.user or self.email}"

    @classmethod
    def post_save_dispatch(cls, sender, instance, created, **kwargs):
        if created:
            instance.send_email()
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

        email = self.email or self.user.email

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
            self.create_user_account_after_approval()
            self.refresh_from_db()

        self.send_email(address=self.user.coin_accounts.get(type=self.crypto_type).pub_address)

    def on_decline(self):
        self.send_email()

    def create_user_account_after_approval(self):
        assert self.user is None

        if self.state == self.APPROVED_STATE:
            get_user_model().objects.create_user(
                username=self.email,
                email=self.email,
                password=generate_random_string(),
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


models.signals.post_save.connect(LoanApplication.post_save_dispatch, sender=LoanApplication)
models.signals.post_save.connect(
    LoanApplication.connect_to_user_after_creation,
    sender=settings.AUTH_USER_MODEL
)
