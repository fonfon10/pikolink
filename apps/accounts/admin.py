from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'email_verified', 'is_super_admin', 'is_active')
    list_filter = ('is_super_admin', 'email_verified', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
