from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("nova.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
] + i18n_patterns(
    path("admin/", admin.site.urls),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
