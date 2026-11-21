from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from movies.sitemaps import MovieSitemap, StaticViewSitemap
from movies.views import robots_txt

sitemaps = {"static": StaticViewSitemap, "movies": MovieSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),

    # Wrapper first → owns "/" and "/download/"
    path("", include("wrapper.urls")),

    # Movies app for /watch/, /play/, /stream/, /catalogue/, etc.
    path("catalogue/", include("movies.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
