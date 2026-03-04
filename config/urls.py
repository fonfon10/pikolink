from django.contrib import admin
from django.urls import path, include

from apps.links import views as link_views

urlpatterns = [
    path('', include('apps.links.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('teams/', include('apps.teams.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('django-admin/', admin.site.urls),
    # Short-link redirect MUST be last
    path('<str:short_code>/', link_views.redirect_link, name='redirect_link'),
]
