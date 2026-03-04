from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.links.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('teams/', include('apps.teams.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('django-admin/', admin.site.urls),
]
