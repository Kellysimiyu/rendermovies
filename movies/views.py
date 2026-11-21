from django.conf import settings
from django.contrib import messages
from django.db.models import Q, F
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_GET

from .adblock import clean_url, is_ad_url
from .forms import SearchForm
from .models import AppRelease, Movie
from .stream import resolve_stream


def index(request):
    form = SearchForm(request.GET or None)
    qs = Movie.objects.all()
    if form.is_valid() and form.cleaned_data["q"]:
        q = form.cleaned_data["q"]
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, "movies/index.html", {
        "form": form,
        "featured": qs.filter(featured=True)[:6],
        "movies": qs[:60],
        "total": Movie.objects.count(),
    })


def play(request, video_id):
    ok = resolve_stream(video_id) is not None
    return render(request, "movies/play.html", {
        "video_id": video_id,
        "stream_ok": ok,
        "stream_url": f"/stream/{video_id}/",
    })


def watch(request, slug):
    import re
    m = get_object_or_404(Movie, slug=slug)
    Movie.objects.filter(pk=m.pk).update(views=F("views") + 1)
    hit = re.search(r"(?:v=|youtu\.be/|/embed/)([\w-]{11})", m.video_url or "")
    if not hit:
        raise Http404("no video id")
    return redirect("movies:play", video_id=hit.group(1))


def download(request):
    phone = AppRelease.objects.filter(platform="phone", is_current=True).first()
    tv = AppRelease.objects.filter(platform="androidtv", is_current=True).first()
    return render(request, "movies/download.html", {"phone": phone, "tv": tv})


def download_file(request, pk):
    rel = get_object_or_404(AppRelease, pk=pk)
    try:
        f = rel.apk.open("rb")
    except FileNotFoundError:
        raise Http404("APK missing")
    resp = FileResponse(f, as_attachment=True,
                        filename=f"MovieZone-v{rel.version}-{rel.platform}.apk")
    resp["Content-Type"] = "application/vnd.android.package-archive"
    return resp


@require_POST
def toggle_adblock(request):
    current = request.session.get("adblock", True)
    request.session["adblock"] = not current
    messages.success(request, "Ad-blocker turned " + ("OFF" if current else "ON"))
    return redirect(request.META.get("HTTP_REFERER", "movies:index"))


@require_GET
def robots_txt(request):
    base = settings.SITE_URL.rstrip("/")
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /stream/",
        "Disallow: /adblock/",
        "",
        f"Sitemap: {base}/sitemap.xml",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
