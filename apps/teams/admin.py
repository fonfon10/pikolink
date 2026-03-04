from django.contrib import admin

from .models import Team, TeamMembership


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner', 'created_at')
    search_fields = ('name', 'slug')
    inlines = [TeamMembershipInline]
