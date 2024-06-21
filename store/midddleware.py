# middleware.py

from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from django.middleware.csrf import _get_new_csrf_string

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_response(self, request, response):
        # Call parent's process_response method
        response = super().process_response(request, response)

        # Check if the response indicates a CSRF token failure
        if response.status_code == 403 and response.content == b'CSRF verification failed.':
            # Refresh the CSRF token using the CSRF_COOKIE_NAME setting
            csrf_token = _get_new_csrf_string()
            response.cookies[settings.CSRF_COOKIE_NAME] = csrf_token

        return response
