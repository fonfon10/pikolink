from django.urls import path

from . import views

app_name = 'analytics'

urlpatterns = [
    path('api/recent-clicks/', views.recent_clicks_api, name='recent_clicks_api'),
    path('realtime/', views.realtime, name='realtime'),
]
