import re
import requests
from django.conf import settings
from django.http import StreamingHttpResponse, Http404

AD_PATTERNS = [re.compile(p, re.I) for p in settings.ADBLOCK_BLOCKED_HOSTS]
CHUNK = 1024 * 256
UA = "Mozilla/5.0 (MovieZone/1.0)"


def is_ad_request(url):
    return any(p.search(url) for p in AD_PATTERNS)


def stream(request, video_id):
    from .stream import resolve_stream
    upstream = resolve_stream(video_id)
    if not upstream:
        raise Http404("stream unavailable")
    if is_ad_request(upstream):
        raise Http404("ad stream blocked")

    headers = {"User-Agent": UA}
    if "HTTP_RANGE" in request.META:
        headers["Range"] = request.META["HTTP_RANGE"]

    try:
        r = requests.get(upstream, headers=headers, stream=True, timeout=30)
    except requests.RequestException:
        raise Http404("upstream unreachable")

    def gen():
        for chunk in r.iter_content(CHUNK):
            if chunk:
                yield chunk

    resp = StreamingHttpResponse(gen(), status=r.status_code,
                                 content_type=r.headers.get("Content-Type", "video/mp4"))
    for h in ("Content-Length", "Content-Range", "Accept-Ranges"):
        if h in r.headers:
            resp[h] = r.headers[h]
    resp["Cache-Control"] = "no-store"
    return resp
