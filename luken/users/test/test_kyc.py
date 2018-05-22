import json
import mock
from django.test import TestCase, override_settings
from django.urls import reverse
from django.forms.models import model_to_dict
from django.core.files.storage import Storage
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from .factories import UserFactory
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from nose.tools import ok_, eq_
from .. import views
from .. import models 



file_mock = mock.MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'

storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
storage_mock.url = mock.MagicMock(name='url')
storage_mock.url.return_value = '/tmp/test1.jpg'

@override_settings(COIN_BACKENDS={
    "Bitcoin": "luken.coins.test.TestBackend",
    "Ethereum": "luken.coins.test.TestBackend"
})
class KYCApiTestCase(APITestCase):
    @mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock)
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('kyc_form')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.kyc = models.KYC(user=self.user,
                              user_fullname = "John Doe",
                              phone_number = "+995598008517",
                              source_of_funds = "1",
                              loan_for = 0,
                              bank_info_name = "Sample Name",
                              bank_info_inst_number = 55,
                              bank_info_routing = 1,
                              bank_info_account_number=5,
                              swift_code = "swiftcode",
                              photo_id = file_mock ,
                              proof_of_address = file_mock,
                              selfie = file_mock,
                              country = "USA",
                              street_address = "Sample Street Address",
                              city = "New York",
                              state_province = "State",
                              postal_zip_code = "1234"

                                )

    def test_post_request_creates_an_entry_kyc(self):
        response = self.client.post(self.url,model_to_dict(self.kyc))

        eq_(response.status_code,201)

    
    def test_post_can_be_retrieved_after_post_request(self):
        self.client.post(self.url,model_to_dict(self.kyc))
        response = self.client.get(self.url,{})

        kyc_id = response.json()['results'][0]['id']
        retrieve_resp = self.client.get(reverse('kyc_form_retrieve',kwargs = {'pk': kyc_id }))

        eq_(retrieve_resp.status_code,200)


    def test_post_can_be_updated(self):
        self.client.post(self.url,model_to_dict(self.kyc))
        response = self.client.get(self.url,{})

        kyc_id = response.json()['results'][0]['id']
        patch_resp = self.client.patch(reverse('kyc_form_retrieve',kwargs = {'pk': kyc_id }),data = {'city':'London'},kwargs = {'pk': kyc_id })
        eq_(patch_resp.status_code,200)

    def test_post_can_be_deleted(self):
        self.client.post(self.url,model_to_dict(self.kyc))
        response = self.client.get(self.url,{})

        kyc_id = response.json()['results'][0]['id']
        patch_resp = self.client.delete(reverse('kyc_form_retrieve',kwargs = {'pk': kyc_id }),data = {'city':'London'},kwargs = {'pk': kyc_id })
        eq_(patch_resp.status_code,204)    