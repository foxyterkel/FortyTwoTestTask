from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import View
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from PIL import Image
import StringIO
from io import BytesIO
import base64
import uuid
import re
from django.http import Http404
import logging
from django.core.exceptions import ObjectDoesNotExist

from apps.contact.models import Contact, RequestEntry
from django.conf import settings
from apps.contact.forms import EditForm

logr = logging.getLogger(__name__)


class Main(View):
    def get(self, request):
        logr.info(request.path)
        try:
            bio = Contact.objects.get(email=settings.EMAIL_FOR_MAIN_PAGE)
        except ObjectDoesNotExist:
            raise Http404
        logr.debug(bio)
        return render(request, 'index.html', {'bio': bio})


class RequestSpy(View):
    def get(self, request):
        RequestEntry.objects.filter(watched=False).update(watched=True)
        last_requests = RequestEntry.objects.all()[:10]
        logr.debug([i.url_path for i in last_requests])
        return render(request, 'request.html', {'last_requests':
                                                last_requests})


class UpdaterUnactive(View):
    def get(self, request):
        unmarked = RequestEntry.objects.filter(watched=False)
        return HttpResponse(len(unmarked))


class UpdaterActive(View):
    def get(self, request):
        unmarked = RequestEntry.objects.filter(watched=False)
        res = []
        for i in unmarked:
            res.append([i.url_path, i.created_at.strftime('%b. %d, %Y, %H:%M')])
        res.reverse()
        data = {'requests': res, 'number': len(unmarked)}
        RequestEntry.objects.filter(watched=False).update(watched=True)
        return HttpResponse(json.dumps(data), content_type='application/json')


class Editor(View):
    def get(self, request):
        filing = get_object_or_404(Contact, email=settings.EMAIL_FOR_MAIN_PAGE)
        form = EditForm(instance=filing)
        photo = filing.photo
        return render(request, 'edit.html', {'form': form, 'photo': photo})

    def post(self, request):
        form = request.POST.get('form')
        image_json = request.POST.get('image')
        data = json.loads(form)
        new_data = {}
        for i in data:
            new_data[i['name']] = i['value']
        id = Contact.objects.get(email=settings.EMAIL_FOR_MAIN_PAGE)
        edit_form = EditForm(new_data, instance=id)
        if edit_form.is_valid():
            edit_form.save()
            if image_json != 'null':
                photo_file = prepare_picture(image_json)
                id.photo = photo_file
                id.save()
            return HttpResponse('Saved! Your model was updated.')
        return HttpResponse(edit_form.errors)


def prepare_picture(json_data):
    data = json.loads(json_data)
    ext_info, ready_data = data.split(',')
    ext = re.search('image/(\w+);', ext_info).group(1)
    image = Image.open(BytesIO(base64.b64decode(ready_data)))
    image.thumbnail(settings.IMAGE_SIZE, Image.ANTIALIAS)
    photo_io = StringIO.StringIO()
    image.save(photo_io, format='%s' % (ext))
    photo_file = InMemoryUploadedFile(photo_io, 'photo', generate_name(ext),
                                      'image/%s' % (ext), photo_io.len, None)
    return photo_file


def generate_name(ext):
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return filename
