from django.urls import path
from . import views
from . import proxy as stream_proxy

app_name = "movies"

urlpatterns = [
    path("", views.index, name="index"),
    path("watch/<slug:slug>/", views.watch, name="watch"),
    path("play/<str:video_id>/", views.play, name="play"),
    path("stream/<str:video_id>/", stream_proxy.stream, name="stream"),
    path("download/", views.download, name="download"),
    path("download/<int:pk>/file/", views.download_file, name="download_file"),
    path("adblock/toggle/", views.toggle_adblock, name="toggle_adblock"),
]
