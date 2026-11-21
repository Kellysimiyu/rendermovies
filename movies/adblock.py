from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from django.conf import settings

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "dclid", "msclkid", "yclid",
    "ad_id", "adset_id", "campaign_id", "aff_id", "affid", "ref", "referrer",
}


def is_ad_url(url):
    if not url:
        return False
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return True
    return any(host == b or host.endswith("." + b) for b in settings.ADBLOCK_BLOCKED_HOSTS)


def clean_url(url):
    if not url:
        return url
    parsed = urlparse(url)
    if is_ad_url(url):
        return ""
    kept = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
            if k.lower() not in TRACKING_PARAMS]
    return urlunparse(parsed._replace(query=urlencode(kept)))


def adblock_context(request):
    if "adblock" not in request.session:
        request.session["adblock"] = True
    return {
        "adblock_enabled": request.session["adblock"],
        "adblock_csp": settings.ADBLOCK_CSP,
    }
