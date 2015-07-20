from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from PIL import Image
import StringIO
from io import BytesIO
import base64
import uuid
import re

from apps.contact.models import Contact, MyMiddle
from fortytwo_test_task.settings import EMAIL_FOR_MAIN_PAGE, IMAGE_SIZE
from apps.contact.forms import EditForm


class Main(View):
    def get(self, request):
        bio = Contact.objects.get(email=EMAIL_FOR_MAIN_PAGE)
        return render(request, 'index.html', {'bio': bio})


class RequestSpy(View):
    def get(self, request):
        unmarked = MyMiddle.objects.filter(watched=False)
        for i in unmarked:
            i.watched = True
            i.save()
        ten_request = MyMiddle.objects.all()[:10]
        return render(request, 'request.html', {'ten_request': ten_request})


class Updater(View):
    def get(self, request):
        unmarked = MyMiddle.objects.filter(watched=False)
        if unmarked:
            return HttpResponse(unmarked.__len__())
        else:
            return HttpResponse(0)


class Editor(View):
    def get(self, request):
        filing = Contact.objects.get(email=EMAIL_FOR_MAIN_PAGE)
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
        id = Contact.objects.get(email=EMAIL_FOR_MAIN_PAGE)
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
    image.thumbnail(IMAGE_SIZE, Image.ANTIALIAS)
    photo_io = StringIO.StringIO()
    image.save(photo_io, format='%s' % (ext))
    photo_file = InMemoryUploadedFile(photo_io, 'photo', generate_name(ext),
                                      'image/%s' % (ext), photo_io.len, None)
    return photo_file


def generate_name(ext):
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return filename
