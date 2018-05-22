from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken import views

from luken.coins.urls import coins_router
from luken.loan.urls import loan_router

from luken.users.views import kyc_webhook
from luken.xpub.views import txhash_webhook

schema_view = get_swagger_view(title='Luken API')

api = DefaultRouter()
api.registry.extend(coins_router.registry)
api.registry.extend(loan_router.registry)

api_urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path("", include(api.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-docs/', schema_view),
    path('jot_form_webhook/', kyc_webhook, name='kyc_webhook'),
    path("txhash-webhook", txhash_webhook, name="txhash-webhook"),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
