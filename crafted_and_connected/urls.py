from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crafted_and_connected.store.urls')),
    path('accounts/', include('crafted_and_connected.authentication.urls')),
    path('post/', include('crafted_and_connected.social.urls')),
    path('chat/', include('crafted_and_connected.messaging.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
