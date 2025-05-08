from django.http import JsonResponse
from rest_framework import status


class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_token = request.headers.get('x-token')

        if not x_token or len(x_token) != 32:
            return JsonResponse(
                {"detail": "Invalid x-token header. It should contain exactly 32 characters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = self.get_response(request)
        return response
