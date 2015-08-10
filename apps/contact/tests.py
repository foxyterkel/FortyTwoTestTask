# -*- coding: utf-8 -*-
"""
Django unit test for project fortytwo_test_task
Making client and superuser in setUp
each test for differnt parts of project
can be start as separare test
"""

from django.test import TestCase
import re

from fortytwo_test_task.settings import EMAIL_FOR_MAIN_PAGE
from apps.contact.forms import EditForm
from apps.contact.models import Contact, RequestEntry, Signal
from apps.contact.templatetags.admin_editor import admin_editor_url


class Tester(TestCase):

    def test_main(self):
        """
        test_main for testing entry in base.
        """

        contact = Contact.objects.all()
        self.assertEqual(len(contact), 1)
        self.assertEqual(contact[0].first_name, 'Sergii')

    def test_main_context(self):
        """
        Testing main page status code, and page context.
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['bio'], Contact)

    def test_main_with_unicode(self):
        """
        Testing main page with unicode entry.
        """

        Contact.objects.all().delete()
        Contact.objects.create(first_name=u'Їжак', last_name=u'Євлампій',
                               email=u'terkel919@gmail.com',
                               contacts=u'+380662352011',
                               bio=u'My little story!')
        response = self.client.get('/')
        self.assertIn('Їжак', response.content)
        self.assertIn('Євлампій', response.content)
        self.assertIn('+380662352011', response.content)
        self.assertIn('My little story', response.content)
        self.assertIn('terkel919@gmail.com', response.content)

    def test_main_page(self):
        """
        test_main_page for testing main page.
        """
        response = self.client.get('/')
        self.assertIn('Sergii', response.content)
        self.assertIn('Vanzha', response.content)
        self.assertIn('+380662352011', response.content)
        self.assertIn('My little story', response.content)
        self.assertIn('terkel919@gmail.com', response.content)

    def test_main_page_with_two_entry(self):
        """
        test_main_page for testing main page. When 2 entry in base.

        """
        self.create_other_user()
        response = self.client.get('/')
        self.assertIn('Sergii', response.content)
        self.assertIn('terkel919@gmail.com', response.content)
        self.assertNotIn('Andrii', response.content)
        self.assertNotIn('andrii@mail.ru', response.content)

    def test_main_page_with_zero_entry(self):
        """
        test_main_page for testing main page. When no entry in base.
        """

        Contact.objects.all().delete()
        response = self.client.get('/')
        self.assertIn('Page Not Found', response.content)
        self.assertEqual(response.status_code, 404)

    def test_main_page_with_wrong_email(self):
        """
        test_main_page for testing main page. When in base one entry,
        but wrong email.
        """

        Contact.objects.all().delete()
        self.create_other_user()
        response = self.client.get('/')
        self.assertIn('Page Not Found', response.content)
        self.assertEqual(response.status_code, 404)

    def test_request_spy_for_creating(self):
        """
        test_request_spy for testing spy.
        Checking status code, and RequestEntry.objects.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'index.html')
        watched = RequestEntry.objects.filter(watched=False)
        self.assertNotEqual(watched.__len__(), 0)

    def test_request_spy_for_marking(self):
        """
        test_request_spy for testing spy.
        Checking status code, and RequestEntry.objects marking.
        """

        response = self.client.get('/spy/')
        watched = RequestEntry.objects.filter(watched=False)
        self.assertEqual(watched.__len__(), 0)
        self.assertIn('/spy/', response.content)

    def test_request_spy_empty_middle(self):
        """
        test_request_spy for testing spy.
        Checking status code, and RequestEntry. Empty middle.
        """
        RequestEntry.objects.all().delete()
        response = self.client.get('/spy/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/spy/', response.content)

    def test_request_spy_all_watched(self):
        """
        test_request_spy for testing spy.
        Checking status code, and RequestEntry. All watched.
        """
        for i in RequestEntry.objects.all():
            i.watched = False
            i.save()
        response = self.client.get('/spy/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/spy/', response.content)

    def test_request_spy_all_unwatched(self):
        """
        test_request_spy for testing spy.
        Checking status code, and RequestEntry. All unwatched.
        """
        for i in RequestEntry.objects.all():
            i.watched = True
            i.save()
        response = self.client.get('/spy/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/spy/', response.content)

    def test_request_spy_entry(self):
        """
        test_request_spy for testing spy.
        Checking status code, and RequestEntry. testing entry.
        """
        self.client.get('/admin/')
        self.client.get('/edit/')
        response = self.client.get('/spy/')
        self.assertIn('/admin/', response.content)
        self.assertIn('/edit/', response.content)

    def test_auth_pass(self):
        """
        Authentication test.
        """
        response = self.client.post('/account/login/', {'username': 'admin',
                                                        'password': 'admin'})
        self.assertEqual(response.status_code, 302)

    def test_auth_fail(self):
        """
        Authentication test.
        """
        response = self.client.post('/account/login/', {'username': 'admyn',
                                                        'password': 'admin'})
        self.assertEqual(response.status_code, 200)

    def test_editor_with_sergii(self):
        """
        Testing edit page.
        """
        responce = self.client.get('/edit/')
        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce.context['form'], EditForm)
        self.assertIn('Sergii', responce.content)

    def test_editor_without_sergii(self):
        """
        Testing edit page.
        """
        Contact.objects.all().delete()
        responce = self.client.get('/edit/')
        self.assertIn('Page Not Found', responce.content)

    def test_editor_without_sergii_rename(self):
        """
        Testing edit page.
        """
        sergii = Contact.objects.get(email=EMAIL_FOR_MAIN_PAGE)
        sergii.first_name = 'Andrii'
        sergii.save()
        responce = self.client.get('/edit/')
        self.assertIn('Andrii', responce.content)

    def test_editor_without_andrii(self):
        """
        Testing edit page.
        """
        Contact.objects.all().delete()
        self.create_other_user()
        responce = self.client.get('/edit/')
        self.assertIn('Page Not Found', responce.content)

    def test_admin_editor_contact(self):
        """
        Testing castom template tags.
        """
        contact = Contact.objects.all()[0]
        url = re.search("href=(\S+)>", admin_editor_url(contact)).group(1)
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, 200)

    def test_admin_editor_middle(self):
        """
        Testing castom template tags.
        """
        middle = RequestEntry.objects.all()[0]
        url = re.search("href=(\S+)>", admin_editor_url(middle)).group(1)
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, 200)

    def test_signal_create(self):
        """
        testing signal create.
        """
        self.create_other_user()
        count = Signal.objects.all().__len__()
        self.assertNotEqual(count, 0)
        latest = Signal.objects.last()
        self.assertEqual(latest.action, 'create')

    def test_signal_delete(self):
        """
        testing signal delete.
        """
        Contact.objects.all().delete()
        latest = Signal.objects.last()
        self.assertEqual(latest.action, 'delete')

    def test_signal_save(self):
        """
        testing signal save.
        """
        sergii = Contact.objects.get(email=EMAIL_FOR_MAIN_PAGE)
        sergii.first_name = 'Andrii'
        sergii.save()
        latest = Signal.objects.last()
        self.assertEqual(latest.action, 'save')

    def create_other_user(self):
        Contact.objects.create(first_name='Andrii', last_name='Vanzha',
                               email='andrii@mail.ru',
                               contacts='+380662453012',
                               bio='His little story!')
