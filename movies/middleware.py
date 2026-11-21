from django.conf import settings


class AdBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        enabled = request.session.get("adblock", True) if hasattr(request, "session") else True
        if enabled:
            response["Content-Security-Policy"] = settings.ADBLOCK_CSP
            response["X-Adblock"] = "on"
        else:
            response["X-Adblock"] = "off"
        return response
