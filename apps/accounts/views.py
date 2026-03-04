from datetime import timedelta

from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from apps.accounts.decorators import super_admin_required
from apps.accounts.models import CustomUser
from apps.analytics.models import Click
from apps.links.models import Link
from apps.teams.models import Team


@super_admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    week_ago = timezone.now() - timedelta(days=7)
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_links': Link.objects.count(),
        'clicks_today': Click.objects.filter(
            clicked_at__date=today
        ).count(),
        'new_signups_7d': CustomUser.objects.filter(
            date_joined__gte=week_ago
        ).count(),
    }
    return render(request, 'superadmin/dashboard.html', {'stats': stats})


@super_admin_required
def admin_users(request):
    users = (
        CustomUser.objects.all()
        .annotate(link_count=Count('links'))
        .order_by('-date_joined')
    )
    return render(request, 'superadmin/users.html', {'users': users})


@super_admin_required
def admin_links(request):
    links = (
        Link.objects.all()
        .select_related('owner')
        .order_by('-created_at')
    )
    return render(request, 'superadmin/links.html', {'links': links})


@super_admin_required
def admin_teams(request):
    teams = (
        Team.objects.all()
        .select_related('owner')
        .annotate(
            member_count=Count('memberships'),
        )
        .order_by('-created_at')
    )
    return render(request, 'superadmin/teams.html', {'teams': teams})
