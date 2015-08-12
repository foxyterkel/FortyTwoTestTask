__author__ = 'tyler'
from apps.contact.models import RequestEntry


class RequestSpyMiddleWare():
    def process_request(self, request):
        if not request.is_ajax():
            RequestEntry.objects.create(url_path=request.path)
        return None
