import json
from django.test import TestCase, override_settings
from django.urls import reverse
from .factories import UserFactory
import mock


@override_settings(COIN_BACKENDS={
    "Bitcoin": "luken.coins.test.TestBackend",
    "Ethereum": "luken.coins.test.TestBackend"
})
class WebhookTestCase(TestCase):

    @mock.patch('luken.users.views.Pusher')
    def test_webhook_successfull(self, pusher_mock):
        user = UserFactory()
        self.client.post(reverse('kyc_webhook'), {
            'rawRequest': json.dumps({"q15_userid": str(user.pk)})})

        kyc = user.kyc_set.first()
        user.refresh_from_db()

        self.assertEquals(kyc.user.pk, user.pk)
        self.assertTrue(user.kyc_applied)
        
        pusher_mock.from_env.return_value.trigger.assert_called()
