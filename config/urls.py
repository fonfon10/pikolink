from django.contrib import admin
from django.urls import path, include

from apps.accounts import views as account_views
from apps.links import views as link_views

urlpatterns = [
    path('', include('apps.links.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('teams/', include('apps.teams.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('super-admin/', account_views.admin_dashboard, name='super_admin_dashboard'),
    path('super-admin/users/', account_views.admin_users, name='super_admin_users'),
    path('super-admin/links/', account_views.admin_links, name='super_admin_links'),
    path('super-admin/teams/', account_views.admin_teams, name='super_admin_teams'),
    path('django-admin/', admin.site.urls),
    # Short-link redirect MUST be last
    path('<str:short_code>/', link_views.redirect_link, name='redirect_link'),
]
