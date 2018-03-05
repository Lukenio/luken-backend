from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import (
    loader,
    Context,
)


plaintext = loader.get_template("loan/email.txt")
html = loader.get_template("loan/email.html")


class LoanApplication(models.Model):
    TERMS_MONTH_CHOICES = (
        (0, "3 Month"),
        (1, "6 Month"),
        (2, "12 Month"),
    )

    STATE_CHOICES = (
        (0, "Submitted"),
        (1, "In Review"),
        (2, "Approved"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    email = models.EmailField(blank=True)
    loaned_amount = models.DecimalField(decimal_places=2, max_digits=20)
    bitcoin_collateral = models.DecimalField(decimal_places=8, max_digits=20)
    bitcoin_price_usd = models.DecimalField(decimal_places=2, max_digits=20)
    terms_month = models.SmallIntegerField(choices=TERMS_MONTH_CHOICES)
    state = models.SmallIntegerField(choices=STATE_CHOICES)

    def __str__(self):
        return f"Loan Application - {self.user or self.email}"

    @classmethod
    def send_email(cls, sender, instance, created, **kwargs):
        if not instance.email or not created:
            return

        ctx = Context({"loan": instance})

        text_content = plaintext.render(ctx)
        html_content = html.render(ctx)

        msg = EmailMultiAlternatives(
            "Mail about Loan Application",
            text_content,
            "Loan Application mail sender (should be in settings, I guess)",
            [instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


models.signals.post_save.connect(LoanApplication.send_email, sender=LoanApplication)
