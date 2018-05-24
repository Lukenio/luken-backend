from django.conf import settings
from hellosign_sdk import HSClient


client = HSClient(api_key=settings.HELLO_SIGN_API_KEY)

template_id = "0558d2f6c9f02acf7f16422f69582ff72cb810f7"
