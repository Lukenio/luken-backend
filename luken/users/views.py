import logging
import json
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import User, KYC
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest


logger = logging.getLogger(__name__)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrives user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


@require_POST
@csrf_exempt
def kyc_webhook(request):
    data = request.POST.dict()

    if data.get('rawRequest'):
        data = json.loads(data['rawRequest'])

        user_id = data['q15_userid']
        kyc = KYC.objects.create(jot_form_data=data, user_id=user_id)

        kyc.user.kyc_applied = True
        kyc.user.save()

        return HttpResponse('Ok')

    return HttpResponseBadRequest('bad request')
