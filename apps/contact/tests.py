"""
Django unit test for project fortytwo_test_task
Making client and superuser in setUp
each test for differnt parts of project
can be run as separare test
"""

from django.test.client import Client
import unittest
from django.contrib.auth.models import User

from apps.contact.models import Contact


class ModelTester(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create(username='admin', password='admin')

    def tearDown(self):
        Contact.objects.all().delete()
        User.objects.all().delete()

    #test for main page

    def test_main(self):
        contact = Contact.objects.all()
        self.assertEqual(contact.__len__(), 1)
        self.assertEqual(contact[0].first_name, 'Sergii')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['bio'], Contact)
