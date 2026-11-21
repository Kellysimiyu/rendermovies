from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Home + download pages."""
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return ["wrapper:movies", "wrapper:download", "movies:index", "movies:download"]

    def location(self, item):
        return reverse(item)


class MovieSitemap(Sitemap):
    """Every movie in the Django catalogue."""
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        from .models import Movie
        return Movie.objects.all().order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()
