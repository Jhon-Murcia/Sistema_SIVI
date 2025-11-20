# autenticacion/middleware.py
from django.utils import translation

class ForceSpanishMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate('es')
        response = self.get_response(request)
        translation.deactivate()
        return response
