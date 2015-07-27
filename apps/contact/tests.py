"""
Django unit test for project fortytwo_test_task
Making client and superuser in setUp
each test for differnt parts of project
can be start as separare test
"""

from django.test.client import Client
import unittest

from apps.contact.models import Contact, MyMiddle


class ModelTester(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_main(self):
        """
        test_main for testing main page. Can be start separate.
        """

        contact = Contact.objects.all()
        self.assertEqual(contact.__len__(), 1)
        self.assertEqual(contact[0].first_name, 'Sergii')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['bio'], Contact)

    def test_request_spy(self):
        """
        test_request_spy for testing spy. Can be start separate.
        Checking status code, and MyMiddle.objects.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'index.html')
        watched = MyMiddle.objects.filter(watched=False)
        self.assertNotEqual(watched.__len__(), 0)
        response = self.client.get('/spy/')
        watched = MyMiddle.objects.filter(watched=False)
        self.assertEqual(watched.__len__(), 0)

    def test_auth(self):
        """
        Authentication test
        """
        response = self.client.post('/account/login/', {'username': 'admin',
                                                        'password': 'admin'})
        self.assertEqual(response.status_code, 302)
