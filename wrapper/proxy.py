"""
Optional server-side proxy + ad-block function.

Only needed if a wrapped GitHub site refuses to load inside an iframe.
It fetches the remote HTML, strips <script> tags pointing at known ad hosts,
removes tracking params, and rewrites relative links so they resolve.
"""
import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

TIMEOUT = 15
UA = "Mozilla/5.0 (MovieZoneWrapper/1.0)"


def is_ad_url(url: str) -> bool:
    """Return True if the URL points at a known ad/tracker host."""
    if not url:
        return False
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return True
    return any(host == b or host.endswith("." + b) for b in settings.ADBLOCK_BLOCKED_HOSTS)


def _proxy(request, base_url: str, path: str) -> HttpResponse:
    target = urljoin(base_url, path or "")
    if not target.startswith(base_url):
        return HttpResponseBadRequest("bad target")
    try:
        r = requests.get(target, timeout=TIMEOUT, headers={"User-Agent": UA})
    except requests.RequestException:
        return HttpResponseBadRequest("upstream unreachable")

    ctype = r.headers.get("Content-Type", "text/html")
    # Pass binary assets through untouched
    if not ctype.startswith("text/html"):
        return HttpResponse(r.content, content_type=ctype, status=r.status_code)

    soup = BeautifulSoup(r.text, "html.parser")

    # ---- ad-block: drop ad scripts/iframes ----
    for tag in soup.find_all(["script", "iframe", "ins"]):
        src = tag.get("src") or tag.get("data-src") or ""
        if is_ad_url(src):
            tag.decompose()

    # ---- rewrite relative links so they hit the proxy ----
    prefix = request.path.rsplit("/", 1)[0] + "/"
    for tag, attr in (("a","href"),("link","href"),("script","src"),
                      ("img","src"),("iframe","src")):
        for el in soup.find_all(tag):
            v = el.get(attr)
            if not v or v.startswith(("http://","https://","#","data:","mailto:")):
                continue
            el[attr] = urljoin(prefix, v)

    return HttpResponse(str(soup), content_type="text/html; charset=utf-8", status=r.status_code)


def proxy_movies(request, path=""):
    return _proxy(request, settings.MOVIES_SITE_URL, path)


def proxy_download(request, path=""):
    return _proxy(request, settings.DOWNLOAD_SITE_URL, path)
