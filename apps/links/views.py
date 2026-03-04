from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseGone, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render

from apps.analytics.models import Click
from apps.links.models import Link


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    return render(request, 'links/dashboard.html')


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
