from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST


from apps.accounts.decorators import super_admin_required
from apps.accounts.forms import ProfileForm
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
    from allauth.account.models import EmailAddress
    users = (
        CustomUser.objects.all()
        .annotate(link_count=Count('links'))
        .order_by('-date_joined')
    )
    verified_emails = set(
        EmailAddress.objects.filter(verified=True).values_list('email', flat=True)
    )
    for user in users:
        user.is_verified = user.email in verified_emails
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


@super_admin_required
def admin_user_profile(request, user_id):
    from allauth.account.models import EmailAddress
    user = get_object_or_404(CustomUser, pk=user_id)
    user.is_verified = EmailAddress.objects.filter(
        email=user.email, verified=True
    ).exists()
    return render(request, 'superadmin/user_profile.html', {'profile_user': user})


@super_admin_required
@require_POST
def admin_toggle_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'{user.email} has been {status}.')
    return redirect('super_admin_users')


@super_admin_required
@require_POST
def admin_delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if user == request.user:
        messages.error(request, 'You cannot delete yourself.')
        return redirect('super_admin_users')
    email = user.email
    user.delete()
    messages.success(request, f'{email} has been deleted.')
    return redirect('super_admin_users')


@super_admin_required
@require_POST
def admin_reset_password(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    from allauth.account.forms import ResetPasswordForm
    form = ResetPasswordForm(data={'email': user.email})
    if form.is_valid():
        form.save(request)
    messages.success(request, f'Password reset email sent to {user.email}.')
    return redirect('super_admin_users')


@super_admin_required
@require_POST
def admin_change_role(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if user == request.user:
        messages.error(request, 'You cannot change your own role.')
        return redirect('super_admin_users')
    role = request.POST.get('role', '')
    if role == 'super_admin':
        user.is_super_admin = True
        user.is_staff = True
    elif role == 'staff':
        user.is_super_admin = False
        user.is_staff = True
    else:
        user.is_super_admin = False
        user.is_staff = False
    user.save(update_fields=['is_super_admin', 'is_staff'])
    messages.success(request, f'Role updated for {user.email}.')
    return redirect('super_admin_users')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
