from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import loader

import reversion
from reversion.models import Version

from luken.utils.random import generate_random_string


plaintext = loader.get_template("loan/email.txt")
html = loader.get_template("loan/email.html")


@reversion.register()
class LoanApplication(models.Model):
    TERMS_MONTH_CHOICES = (
        (0, "3 Month"),
        (1, "6 Month"),
        (2, "12 Month"),
    )

    SUBMITTED_STATE = 0
    IN_REVIEW_STATE = 1
    APPROVED_STATE = 2
    STATE_CHOICES = (
        (SUBMITTED_STATE, "Submitted"),
        (IN_REVIEW_STATE, "In Review"),
        (APPROVED_STATE, "Approved"),
    )

    TYPES = (
        (0, "Bitcoin"),
        (1, "Etherium"),
    )

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

    def __str__(self):
        return f"Loan Application - {self.user or self.email}"

    @classmethod
    def send_email(cls, sender, instance, created, **kwargs):
        if not instance.email or not created:
            return

        ctx = {"loan": instance}

        text_content = plaintext.render(ctx)
        html_content = html.render(ctx)

        msg = EmailMultiAlternatives(
            "Mail about Loan Application",
            text_content,
            "loan-application@luken.com",
            [instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @classmethod
    def connect_to_user_after_creation(cls, sender, instance, created, **kwargs):
        if not created:
            return

        anonymous_loans = cls.objects.filter(user=None, email=instance.email)
        for loan in anonymous_loans:
            loan.user = instance
            loan.save()

    @classmethod
    def create_user_account_after_approval(cls, sender, instance, created, **kwargs):
        if instance.user is not None or created:
            return

        latest = Version.objects.get_for_object(instance).latest("revision__date_created")

        if instance.state > latest.field_dict["state"] and instance.state == cls.APPROVED_STATE:
            get_user_model().objects.create_user(
                username=instance.email,
                email=instance.email,
                password=generate_random_string(),
            )


models.signals.post_save.connect(LoanApplication.send_email, sender=LoanApplication)
models.signals.post_save.connect(
    LoanApplication.connect_to_user_after_creation,
    sender=settings.AUTH_USER_MODEL
)
models.signals.post_save.connect(LoanApplication.create_user_account_after_approval, sender=LoanApplication)
