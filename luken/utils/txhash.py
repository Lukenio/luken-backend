from django.conf import settings

import requests


TRACKER_API_URL = "https://stage.app.txhash.com/api/trackers"


def create_tracker(name, coin, address, http_url, http_method="GET"):
    payload = {
        "name": name,
        "smartContract": False,
        "coin": coin,
        "address": address,
        "action": {
            "code": "http-request",
            "httpUrl": http_url,
            "httpMethod": http_method
        }
    }
    r = requests.post(TRACKER_API_URL,
                      json=payload,
                      headers={
                          "Authorization": f"Key {settings.TXHASH_API_KEY}"
                      })

    if r.status_code != 201:
        raise RuntimeError(
            f"TXHASH returned unexpected status code - {r.status_code}")

    return r.json()
