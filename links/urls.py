from django.urls import path

from .views import (
    home,
    clicks_list,
    create_customer,
    create_link,
    links_list,
    redirect_link,
    signup_disabled,
)

urlpatterns = [
    path("", home, name="home"),

    # App pages
    path("app/links", links_list, name="links_list"),
    path("app/links/new", create_link, name="create_link"),
    path("app/customers/new", create_customer, name="create_customer"),
    path("app/clicks", clicks_list, name="clicks_list"),

    # Invite-only signup block
    path("accounts/signup/", signup_disabled, name="account_signup"),

    # Public redirect
    path("<str:code>/", redirect_link, name="redirect_link"),
]