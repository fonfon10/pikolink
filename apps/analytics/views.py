from django.db.models import Count
from django.http import JsonResponse

from apps.analytics.models import Click


def recent_clicks_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'forbidden'}, status=403)
    links = request.user.links.values_list('id', flat=True)
    clicks = Click.objects.filter(link_id__in=links).order_by('-clicked_at')[:20]
    data = [
        {
            'link': c.link.short_code,
            'country': c.country,
            'city': c.city,
            'time': c.clicked_at.isoformat(),
        }
        for c in clicks.select_related('link')
    ]
    return JsonResponse({'clicks': data})
