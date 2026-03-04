from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from apps.accounts.models import CustomUser
from apps.teams.forms import TeamCreateForm
from apps.teams.models import Team, TeamMembership


@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user
            team.slug = slugify(team.name)
            team.save()
            return redirect('teams:team_dashboard', slug=team.slug)
    else:
        form = TeamCreateForm()
    return render(request, 'teams/team_create.html', {'form': form})


@login_required
def team_dashboard(request, slug):
    team = get_object_or_404(
        Team,
        slug=slug,
    )
    is_owner = team.owner == request.user
    is_member = TeamMembership.objects.filter(team=team, user=request.user).exists()
    if not is_owner and not is_member:
        from django.http import Http404
        raise Http404
    members = TeamMembership.objects.filter(team=team).select_related('user')
    return render(request, 'teams/team_dashboard.html', {
        'team': team,
        'members': members,
        'is_owner': is_owner,
    })


@login_required
def invite_member(request, slug):
    team = get_object_or_404(Team, slug=slug)
    if team.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        email = request.POST.get('email', '')
        role = request.POST.get('role', 'viewer')
        try:
            invitee = CustomUser.objects.get(email=email)
            TeamMembership.objects.get_or_create(
                team=team, user=invitee, defaults={'role': role}
            )
        except CustomUser.DoesNotExist:
            pass
        return redirect('teams:team_dashboard', slug=team.slug)
    return render(request, 'teams/team_invite.html', {'team': team})
