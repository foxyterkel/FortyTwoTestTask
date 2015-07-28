__author__ = 'tyler'
from apps.contact.models import MyMiddle


class MyMiddleWare():
    def process_request(self, request):
        if not request.is_ajax():
            MyMiddle.objects.create(body=request.path)
        return None
