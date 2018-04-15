import uuid

from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class PartnerToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.partner}: {self.id}"
