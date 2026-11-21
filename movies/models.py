from django.db import models
from django.urls import reverse


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=300)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    video_url = models.URLField(help_text="YouTube or direct video URL")
    embed = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movies:watch", args=[self.slug])


class AppRelease(models.Model):
    PLATFORM_CHOICES = [
        ("phone", "Phone"),
        ("androidtv", "Android TV"),
    ]
    version = models.CharField(max_length=20)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    apk = models.FileField(upload_to="apk/")
    size_mb = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    released_at = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-released_at"]

    def __str__(self):
        return f"MovieZone v{self.version} ({self.platform})"
