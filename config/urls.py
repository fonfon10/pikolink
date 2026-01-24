from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # allauth
    path("accounts/", include("allauth.urls")),

    # your app
    path("", include("links.urls")),
]