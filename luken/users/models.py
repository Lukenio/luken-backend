import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
from rest_framework.authtoken.models import Token


@python_2_unicode_compatible
class User(AbstractUser):

    USER_TYPES = [
        ('lander', 'Lander'),
        ('borrower', 'Borrower')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(choices=USER_TYPES, max_length=10)
    kyc_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def get_kyc(self):
        kyc = self.kyc_set.all().order_by('-added').first()
        return kyc.jot_form_data if kyc else None


class KYC(models.Model):
    GENERAL_EXPENCE_LOAN = 0
    STARTING_A_BUSINESS_LOAN = 1
    PURCHASE_MORE_CRYPTOCURRENCY_LOAN = 2
    DEBT_CONSOLIDATION_LOAN = 3
    OTHER_LOAN = 4

    LOAN_CHOICES = (
        (GENERAL_EXPENCE_LOAN, "General Expence"),
        (STARTING_A_BUSINESS_LOAN, "Starting a Business"),
        (PURCHASE_MORE_CRYPTOCURRENCY_LOAN, "Purchase More Cryptocurrency"),
        (DEBT_CONSOLIDATION_LOAN, "Debt Consolidation"),
        (OTHER_LOAN, "Other")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    source_of_funds = models.CharField(max_length=255)
    loan_for = models.SmallIntegerField(choices=LOAN_CHOICES)
    bank_info_name = models.CharField(max_length=255)
    bank_info_inst_number = models.IntegerField()
    bank_info_routing = models.IntegerField()
    bank_info_account_number = models.IntegerField()
    swift_code = models.CharField(max_length=11)
    photo_id = models.FileField(upload_to='photo_id/')
    proof_of_address = models.FileField(upload_to='proof_of_address/')
    selfie = models.FileField(upload_to='selfie/')
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_province = models.CharField(max_length=255)
    postal_zip_code = models.CharField(max_length=15)


    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added']

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=KYC)
def modify_user(sender, instance=None, created=False, **kwargs):
    user = instance.user
    user.first_name = instance.user_fullname.split(" ")[0]
    user.last_name = instance.user_fullname.split(" ")[1]
    user.save()

