from django.urls import path, re_path
from . import views, proxy

app_name = "wrapper"

urlpatterns = [
    path("", views.movies, name="movies"),
    path("download/", views.download, name="download"),
    # Optional proxy fallback (used only if the iframe fails)
    re_path(r"^proxy/movies/(?P<path>.*)$", proxy.proxy_movies, name="proxy_movies"),
    re_path(r"^proxy/download/(?P<path>.*)$", proxy.proxy_download, name="proxy_download"),
]
