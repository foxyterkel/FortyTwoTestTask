__author__ = 'tyler'
from apps.contact.models import RequestEntry


class MyMiddleWare():
    def process_request(self, request):
        if not request.is_ajax():
            RequestEntry.objects.create(body=request.path)
        return None
