import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JsonExceptionMiddleware(MiddlewareMixin):
    """Middleware to format exceptions as JSON responses."""

    def process_exception(self, request, exception):
        response_data = {
            'error5': str(exception),
            'type': exception.__class__.__name__
        }
        # Use the exception's status if available, otherwise default to 404
        status = getattr(exception, 'status', 404)
        return JsonResponse(response_data, status=status)
