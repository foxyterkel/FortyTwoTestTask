__author__ = 'tyler'
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from apps.contact.views import Main, RequestSpy, Updater, Editor
from fortytwo_test_task.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    url(r'^$', Main.as_view()),
    url(r'^spy/$', RequestSpy.as_view()),
    url(r'^updater/$', Updater.as_view()),
    url(r'^edit/$', Editor.as_view()),
    url(r'^account/login/$', login, {'template_name': 'login.html'}),
    url(r'^account/logout/$', logout, {'next_page': '/'}),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
