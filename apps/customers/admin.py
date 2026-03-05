from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company', 'owner', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company')
    list_filter = ('created_at',)
