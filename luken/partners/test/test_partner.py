from django.test import TestCase

from django_dynamic_fixture import G

from ..models import (
    PartnerToken,
    Partner
)


class PartnerTestCase(TestCase):

    def test_creates_default_token(self):
        partner = G(Partner)
        partner_tokens_count = PartnerToken.objects.filter(partner=partner).count()
        self.assertEqual(partner_tokens_count, 1)
