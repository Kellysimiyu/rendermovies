import subprocess
import time
from django.conf import settings

_cache = {}


def _run_ytdlp(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = ["yt-dlp", "-f", "best[ext=mp4]/best", "-g",
           "--no-warnings", "--no-playlist", url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if out.returncode != 0 or not out.stdout.strip():
            return None
        return out.stdout.strip().splitlines()[0]
    except Exception:
        return None


def resolve_stream(video_id):
    now = time.time()
    hit = _cache.get(video_id)
    if hit and hit[1] > now:
        return hit[0]
    url = _run_ytdlp(video_id)
    if url:
        _cache[video_id] = (url, now + 3600)
    return url
