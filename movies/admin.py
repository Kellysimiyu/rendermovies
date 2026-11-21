from django.contrib import admin
from .models import AppRelease, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "embed", "views", "created_at")
    list_filter = ("featured", "embed")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(AppRelease)
class AppReleaseAdmin(admin.ModelAdmin):
    list_display = ("version", "platform", "size_mb", "is_current", "released_at")
    list_filter = ("platform", "is_current")
