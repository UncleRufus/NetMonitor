# Utils
from django.contrib import admin
from django.urls import path, include

# Settings
from .settings import DEBUG

# Views
from apps.dogma_infoseq.views import sigur_request


urlpatterns = [
    path('admin/', admin.site.urls),
    path('visits/', sigur_request, name='sigur_request')
]

if DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
