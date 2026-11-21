from django.conf import settings


def seo(request):
    """Inject SEO defaults into every template."""
    path = request.path if hasattr(request, "path") else "/"
    canonical = settings.SITE_URL.rstrip("/") + path
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DESCRIPTION": settings.SITE_DESCRIPTION,
        "SITE_KEYWORDS": settings.SITE_KEYWORDS,
        "SITE_URL": settings.SITE_URL.rstrip("/"),
        "CANONICAL_URL": canonical,
    }
