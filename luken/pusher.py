import pusher
from django.conf import settings

pusher_client = pusher.Pusher.from_url(settings.PUSHER_URL)
