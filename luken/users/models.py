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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jot_form_data = JSONField()
    added = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
