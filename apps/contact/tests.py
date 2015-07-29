"""
Django unit test for project fortytwo_test_task
Making client and superuser in setUp
each test for differnt parts of project
can be start as separare test
"""

from django.test.client import Client
import unittest
import re


from apps.contact.forms import EditForm
from apps.contact.models import Contact, MyMiddle
from apps.contact.templatetags.admin_editor import admin_editor_url


class ModelTester(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_main(self):
        """
        test_main for testing entry in base. Can be start separate.
        """

        contact = Contact.objects.all()
        self.assertEqual(contact.__len__(), 1)
        self.assertEqual(contact[0].first_name, 'Sergii')

    def test_main_content(self):
        """
        test_main_content for testing main page context. Can be start separate.
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['bio'], Contact)

    def test_main_page(self):
        """
        test_main_page for testing main page. Can be start separate.
        """
        response = self.client.get('/')
        self.assertIn('Sergii', response.content)
        self.assertIn('terkel919@gmail.com', response.content)

    def test_main_page_with_two_entry(self):
        """
        test_main_page for testing main page. When 2 entry in base.
        Can be start separate.
        """
        self.create_other_user()
        response = self.client.get('/')
        self.assertIn('Sergii', response.content)
        self.assertIn('terkel919@gmail.com', response.content)

    def test_main_page_with_zero_entry(self):
        """
        test_main_page for testing main page. When no entry in base.
        Can be start separate.
        """

        Contact.objects.all().delete()
        response = self.client.get('/')
        self.assertIn('Page Not Found', response.content)
        self.restore_user()

    def test_main_page_with_wrong_email(self):
        """
        test_main_page for testing main page. When in base one entry,
        but wrong email. Can be start separate.
        """

        Contact.objects.all().delete()
        self.create_other_user()
        response = self.client.get('/')
        self.assertIn('Page Not Found', response.content)
        Contact.objects.all().delete()
        self.restore_user()

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

    def test_admin_editor(self):
        """
        Testing castom template tags.
        """
        contact = Contact.objects.all()[0]
        url = re.search("href=(\S+)>", admin_editor_url(contact)).group(1)
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, 200)

    def test_editor(self):
        """
        Testing edit page
        """
        responce = self.client.get('/edit/')
        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce.context['form'], EditForm)

    def restore_user(self):
        Contact.objects.create(first_name='Sergii', last_name='Vanza',
                               email='terkel919@gmail.com',
                               contacts='+380662352011',
                               bio='My little story!')

    def create_other_user(self):
        Contact.objects.create(first_name='Andrii', last_name='Vanzha',
                               email='andrii@mail.ru',
                               contacts='+380662453012',
                               bio='His little story!')
