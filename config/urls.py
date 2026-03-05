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
    path('super-admin/users/<int:user_id>/toggle/', account_views.admin_toggle_user, name='super_admin_toggle_user'),
    path('super-admin/users/<int:user_id>/delete/', account_views.admin_delete_user, name='super_admin_delete_user'),
    path('super-admin/users/<int:user_id>/reset-password/', account_views.admin_reset_password, name='super_admin_reset_password'),
    path('super-admin/users/<int:user_id>/change-role/', account_views.admin_change_role, name='super_admin_change_role'),
    path('django-admin/', admin.site.urls),
    # Short-link redirect MUST be last
    path('<str:short_code>/', link_views.redirect_link, name='redirect_link'),
]
