from django.urls import path, include
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

from shareplatform.admin import custom_admin_site

urlpatterns = [
    path('user/', include('user.urls')),
    path('questions/', include('questions.urls')),
    path('groups/', include('groups.urls')),
    path('admin/', custom_admin_site.urls),
    path('', core_views.home, name='home'),
    path('markdownx/', include('markdownx.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
