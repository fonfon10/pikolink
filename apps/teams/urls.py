from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('create/', views.create_team, name='create_team'),
    path('<slug:slug>/', views.team_dashboard, name='team_dashboard'),
    path('<slug:slug>/invite/', views.invite_member, name='invite_member'),
]
