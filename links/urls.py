from django.urls import path

from .views import (
    home,
    create_customer,
    create_link,
    links_list,
    clicks_list,
    redirect_link,
)

urlpatterns = [
    path("", home, name="home"),

    path("app/links", links_list, name="links_list"),
    path("app/links/new", create_link, name="create_link"),

    path("app/customers/new", create_customer, name="create_customer"),

    path("app/clicks", clicks_list, name="clicks_list"),

    # keep this LAST so it never steals routes like /app/...
    path("<str:code>/", redirect_link, name="redirect_link"),
]