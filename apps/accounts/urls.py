from django.urls import path, include

from apps.accounts import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('', include('allauth.urls')),
]
