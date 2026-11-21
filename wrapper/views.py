from django.conf import settings
from django.shortcuts import render


def _no_frame_headers(response):
    """Allow our own pages to be embedded (needed if you ever nest them)."""
    response["X-Frame-Options"] = "SAMEORIGIN"
    return response


def movies(request):
    """Wrap https://kellysimiyu.github.io/Movies/ with ads blocked."""
    resp = render(request, "wrapper/movies.html", {
        "remote_url": settings.MOVIES_SITE_URL,
        "csp": settings.ADBLOCK_CSP,
        "page_title": "Movies",
    })
    resp["Content-Security-Policy"] = settings.ADBLOCK_CSP
    return _no_frame_headers(resp)


def download(request):
    """Wrap https://kellywafula980-afk.github.io/Moviezone/."""
    resp = render(request, "wrapper/download.html", {
        "remote_url": settings.DOWNLOAD_SITE_URL,
        "csp": settings.ADBLOCK_CSP,
        "page_title": "Download App",
    })
    resp["Content-Security-Policy"] = settings.ADBLOCK_CSP
    return _no_frame_headers(resp)
