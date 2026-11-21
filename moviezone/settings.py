from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "wrapper",
    "movies",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "moviezone.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "wrapper" / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
                "movies.seo.seo",
    ]},
}]

WSGI_APPLICATION = "moviezone.wsgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
LANGUAGE_CODE = "en-us"; TIME_ZONE = "Africa/Nairobi"; USE_I18N = True; USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---- The two GitHub sites we wrap ----
MOVIES_SITE_URL   = "https://kellysimiyu.github.io/Movies/"
DOWNLOAD_SITE_URL = "https://kellywafula980-afk.github.io/Moviezone/"

# ---- Ad-block CSP applied to our own pages (and injected into proxy HTML) ----
ADBLOCK_CSP = (
    "default-src 'self' https:; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; "
    "style-src 'self' 'unsafe-inline' https:; "
    "img-src 'self' data: https:; "
    "media-src 'self' https: blob:; "
    "frame-src 'self' https:; "
    "connect-src 'self' https:; "
    "font-src 'self' data: https:; "
    "object-src 'none';"
)
ADBLOCK_BLOCKED_HOSTS = [
    "doubleclick.net","googlesyndication.com","googleadservices.com",
    "adservice.google.com","adnxs.com","taboola.com","outbrain.com",
    "popads.net","propellerads.com","exoclick.com","juicyads.com",
    "trafficjunky.net","adsterra.com","revcontent.com","media.net",
    "criteo.com","pubmatic.com","rubiconproject.com",
]

# ── Custom ad blocker ─────────────────────────────────────────────
YT_DLP_TIMEOUT = 30
STREAM_CACHE_TTL = 3600          # cache resolved stream URLs for 1 hour
AD_BLOCK_HOSTS = [
    "doubleclick.net", "googlesyndication.com", "googleadservices.com",
    "youtube.com/api/stats/ads", "youtube.com/pagead", "youtube.com/ptracking",
    "youtube.com/api/stats/atr", "youtube.com/get_midroll_info",
    "youtube.com/api/stats/qoe", "googlevideo.com/videoplayback/ad",
]

# ── SEO ──────────────────────────────────────────────────────────
SITE_NAME = "MovieZone"
SITE_DESCRIPTION = (
    "Watch free movies, trailers, animations and videos online. "
    "No sign-up, no ads, built-in ad blocker, Android TV ready."
)
SITE_KEYWORDS = (
    "free movies, watch movies online, free movies online, movie streaming, "
    "movie trailers, free films, online movies, ad-free movies, android tv movies, "
    "moviezone, watch free videos"
)
# Change this to your real domain when you deploy
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000")
