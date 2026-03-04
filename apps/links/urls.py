from django.urls import path

from . import views

app_name = 'links'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('links/create/', views.create_link, name='create_link'),
    path('links/<int:pk>/', views.link_detail, name='link_detail'),
]
