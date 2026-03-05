from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseGone, HttpResponseNotAllowed, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render

from apps.analytics.models import Click
from apps.customers.models import Customer
from apps.links.forms import LinkCreateForm
from apps.links.models import Link
from apps.links.utils import generate_short_code


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    links = Link.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'links/dashboard.html', {'links': links})


@login_required
def create_link(request):
    if request.method == 'POST':
        form = LinkCreateForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.owner = request.user
            link.short_code = generate_short_code()
            link.save()
            customer_ids = form.cleaned_data.get('customer_ids', '')
            if customer_ids:
                ids = [int(x) for x in customer_ids.split(',') if x.strip().isdigit()]
                customers = Customer.objects.filter(id__in=ids, owner=request.user)
                link.customers.set(customers)
            return redirect('links:dashboard')
    else:
        form = LinkCreateForm()
    return render(request, 'links/link_create.html', {'form': form})


@login_required
def link_detail(request, pk):
    from datetime import timedelta
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    link = get_object_or_404(Link, pk=pk, owner=request.user)
    top_countries = (
        Click.objects.filter(link=link)
        .exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    top_cities = (
        Click.objects.filter(link=link)
        .exclude(city='')
        .values('city')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    # 30-day click chart data
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_clicks = (
        Click.objects.filter(link=link, clicked_at__gte=thirty_days_ago)
        .annotate(day=TruncDate('clicked_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    max_daily = max((d['count'] for d in daily_clicks), default=1)
    recent_clicks = (
        Click.objects.filter(link=link)
        .order_by('-clicked_at')[:10]
    )
    tagged_customers = link.customers.all()
    return render(request, 'links/link_detail.html', {
        'link': link,
        'top_countries': top_countries,
        'top_cities': top_cities,
        'daily_clicks': daily_clicks,
        'max_daily': max_daily,
        'recent_clicks': recent_clicks,
        'tagged_customers': tagged_customers,
    })


@login_required
def delete_link(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    link = get_object_or_404(Link, pk=pk, owner=request.user)
    link.delete()
    return redirect('links:dashboard')


def _get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _record_click(link, request):
    ip = _get_client_ip(request)
    country, city, cc = '', '', ''
    try:
        from django.contrib.gis.geoip2 import GeoIP2
        g = GeoIP2()
        info = g.city(ip)
        country = info.get('country_name', '')
        city = info.get('city', '')
        cc = info.get('country_code', '')
    except Exception:
        pass
    Click.objects.create(
        link=link,
        ip_address=ip,
        country=country,
        city=city,
        country_code=cc,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referrer=request.META.get('HTTP_REFERER', ''),
    )


def redirect_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code)
    if not link.is_active:
        return HttpResponseGone()
    _record_click(link, request)
    Link.objects.filter(pk=link.pk).update(click_count=link.click_count + 1)
    return HttpResponsePermanentRedirect(link.original_url)
