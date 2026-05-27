from django.http import HttpResponse


class ForceCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")

        allowed_origins = {
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        }

        if request.method == "OPTIONS":
            response = HttpResponse(status=200)
        else:
            response = self.get_response(request)

        if origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"

        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, PATCH, DELETE"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-CSRFToken"

        return response