from django.test.client import Client
import unittest
from django.contrib.auth.models import User
# import re

from apps.contact.models import Contact
# from apps.contact.models import MyMiddle
# from apps.contact.templatetags.admin_editor import admin_editor_url
# from apps.contact.forms import EditForm


class ModelTester(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create(username='admin', password='admin')

    def tearDown(self):
        Contact.objects.all().delete()
        User.objects.all().delete()

    def test_main(self):
        contact = Contact.objects.all()
        self.assertEqual(contact.__len__(), 1)
        self.assertEqual(contact[0].first_name, 'Sergii')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['bio'], Contact)

    # def test_request_spy(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.templates[0].name, 'index.html')
    #     watched = MyMiddle.objects.filter(watched=False)
    #     self.assertNotEqual(watched.__len__(), 0)
    #     response = self.client.get('/spy/')
    #     watched = MyMiddle.objects.filter(watched=False)
    #     self.assertEqual(watched.__len__(), 0)

    # def test_auth(self):
    #     response = self.client.post('/account/login/', {'username': 'admin',
    #                                                     'password': 'admin'})
    #     self.assertEqual(response.status_code, 200)


    # def test_admin_editor(self):
    #     contact = Contact.objects.all()[0]
    #     url = re.search("href=(\S+)>", admin_editor_url(contact)).group(1)
    #     responce = self.client.get(url)
    #     self.assertEqual(responce.status_code, 302)

    # def test_editor(self):
    #     responce = self.client.get('/edit/')
    #     self.assertEqual(responce.status_code, 200)
    #     self.assertIsInstance(responce.context['form'], EditForm)
