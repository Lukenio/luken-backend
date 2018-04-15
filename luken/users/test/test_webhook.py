import json
from django.test import TestCase
from django.urls import reverse
from .factories import UserFactory


class WebhookTestCase(TestCase):

    def test_webhook_successfull(self):
        user = UserFactory()
        self.client.post(reverse('kyc_webhook'), {
            'rawRequest': json.dumps({"q14_userid": str(user.pk)})})

        kyc = user.kyc_set.first()
        user.refresh_from_db()

        self.assertEquals(kyc.user.pk, user.pk)
        self.assertTrue(user.kyc_applied)