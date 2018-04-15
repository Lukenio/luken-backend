import uuid

from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if not created:
            return

        PartnerToken.objects.create(partner=instance)


class PartnerToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.partner}: {self.id}"


models.signals.post_save.connect(Partner.post_save, sender=Partner)
