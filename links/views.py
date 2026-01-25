from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerCreateForm, LinkCreateForm
from .models import Click, Customer, Link


def home(request):
    # Simple landing page.
    # If logged in, go to links list. If not, go to login.
    if request.user.is_authenticated:
        return redirect("links_list")
    return redirect("/accounts/login/")


def signup_disabled(request):
    # Invite-only. No public signup.
    return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def links_list(request):
    links = Link.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "links/links_list.html", {"links": links})


@login_required
def clicks_list(request):
    # Only clicks on the user's own links
    clicks = Click.objects.filter(link__created_by=request.user).order_by("-clicked_at")
    return render(request, "links/clicks_list.html", {"clicks": clicks})


@login_required
def create_link(request):
    """
    Create a link.

    Key behavior:
    - This view reads values from the query string (GET) to pre-fill the form.
    - After creating a customer, we come back here with:
        ?destination_url=...&campaign_name=...&notes=...&customer=<id>
    """
    if request.method == "GET":
        initial = {
            "destination_url": request.GET.get("destination_url", ""),
            "campaign_name": request.GET.get("campaign_name", ""),
            "notes": request.GET.get("notes", ""),
        }

        customer_id = request.GET.get("customer")
        if customer_id:
            try:
                initial["customer"] = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                pass

        form = LinkCreateForm(initial=initial)
        return render(request, "links/create_link.html", {"form": form})

    if request.method == "POST":
        form = LinkCreateForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.created_by = request.user
            link.save()
            return render(request, "links/created.html", {"link": link})

        return render(request, "links/create_link.html", {"form": form})

    return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def create_customer(request):
    """
    Create a customer, then go back to create-link with:
    - same destination_url / campaign_name / notes
    - customer pre-selected to the new one
    """
    next_url = (
        request.GET.get("next")
        or request.POST.get("next")
        or "/app/links/new"
    )

    if request.method == "GET":
        form = CustomerCreateForm()
        return render(
            request,
            "links/create_customer.html",
            {"form": form, "next": next_url},
        )

    if request.method == "POST":
        form = CustomerCreateForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "links/create_customer.html",
                {"form": form, "next": next_url},
            )

        customer = form.save()

        parts = urlparse(next_url)
        qs = parse_qs(parts.query)
        qs["customer"] = [str(customer.id)]
        final_next = urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

        return redirect(final_next)

    return HttpResponseNotAllowed(["GET", "POST"])


def redirect_link(request, code):
    """
    Public redirect endpoint:
      /<code>/
    """
    link = get_object_or_404(Link, code=code)

    Click.objects.create(
        link=link,
        customer=link.customer,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )

    return redirect(link.destination_url, permanent=True)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Click

@login_required
def clicks_list(request):
    clicks = (
        Click.objects
        .filter(link__created_by=request.user)
        .select_related("link", "customer")
        .order_by("-clicked_at")
    )
    return render(request, "links/clicks_list.html", {"clicks": clicks})