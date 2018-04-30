from django.shortcuts import get_object_or_404

from .models import WalletAddress


def txhash_webhook(request):
    address = get_object_or_404(WalletAddress, address=request.GET["address"])
    # TODO: create Transaction or something else
