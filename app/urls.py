from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from mgmt.views import *
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    # path('add_customer/', add_customer, name='add_customer'),
    # path('send_msg/', send_msg, name='send_msg'),

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
