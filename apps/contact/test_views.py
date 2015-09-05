# -*- coding: utf-8 -*-
"""
Django unit test for project fortytwo_test_task
Making client and superuser in setUp
each test for differnt parts of project
can be start as separare test
"""

from django.test import TestCase
import re

from apps.contact.forms import EditForm
from apps.contact.models import Contact, RequestEntry
from apps.contact.templatetags.admin_editor import admin_editor_url


class MainTester(TestCase):

    def test_main_context(self):
        """
        Testing main page status code, and page context.
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bio'], Contact.objects.first())

    def test_with_changed_entry(self):
        """
        Cheking that main page content is'n static.
        We changing entry, and looking for this changes in the main page.
        It prove that main page represent entry.
        """
        sergii = Contact.objects.first()
        sergii.first_name = 'Andrii'
        sergii.save()
        response = self.client.get('/')
        self.assertIn('Andrii', response.content)
        self.assertEqual(response.context['bio'], Contact.objects.first())

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
        self.check_rendered_page_for_content(Contact.objects.first(),
                                             ['first_name', 'last_name',
                                             'contacts', 'bio', 'email'],
                                             response.content, uncode=True)
        self.assertEqual(response.context['bio'], Contact.objects.first())

    def test_main_page(self):
        """
        test_main_page for testing main page.
        """
        response = self.client.get('/')
        self.check_rendered_page_for_content(Contact.objects.first(),
                                             ['first_name', 'last_name',
                                             'contacts', 'bio', 'email'],
                                             response.content)
        self.assertEqual(response.context['bio'], Contact.objects.first())

    def test_main_page_with_two_entry(self):
        """
        test_main_page for testing main page. When 2 entry in base.

        """
        create_other_user()
        response = self.client.get('/')
        self.check_rendered_page_for_content(Contact.objects.first(),
                                             ['first_name', 'last_name',
                                             'contacts', 'bio', 'email'],
                                             response.content)
        self.assertNotIn('Andrii', response.content)
        self.assertNotIn('andrii@mail.ru', response.content)
        self.assertEqual(response.context['bio'], Contact.objects.first())

    def test_main_page_with_zero_entry(self):
        """
        test_main_page for testing main page. When no entry in base.
        """

        Contact.objects.all().delete()
        response = self.client.get('/')
        self.assertIn('Page Not Found', response.content)
        self.assertEqual(response.status_code, 404)

    def check_rendered_page_for_content(self, obj, fields, content,
                                        uncode=False):
        for i in fields:
            if not uncode:
                self.assertIn(getattr(obj, i), content)
            else:
                self.assertIn(getattr(obj, i).encode('utf-8'), content)


class SpyTester(TestCase):

    def test_request_spy_for_marking(self):
        """
        Checking status code of the spy page, and checking for unmarked
        entrys after visiting spy page. Also cheking last url_path on the page.
        """

        response = self.client.get('/spy/')
        watched = RequestEntry.objects.filter(watched=False)
        self.assertEqual(len(watched), 0)
        self.assertIn('/spy/', response.content)

    def test_request_spy_empty_middle(self):
        """
        Checking status code of the spy page if ther is no entry in
        request model.
        """
        RequestEntry.objects.all().delete()
        response = self.client.get('/spy/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/spy/', response.content)

    def test_request_spy_all_watched(self):
        """
        Checking status code of the spy page if every entry in request model
        already watched.
        """
        for i in RequestEntry.objects.all():
            i.watched = True
            i.save()
        response = self.client.get('/spy/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/spy/', response.content)

    def test_request_spy_all_unwatched(self):
        """
        Checking status code of the spy page if every entry im request model
        unwatched.
        """
        for i in RequestEntry.objects.all():
            i.watched = False
            i.save()
        response = self.client.get('/spy/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/spy/', response.content)

    def test_request_spy_entry(self):
        """
        Cheking visited url_path on the page of spy.
        """
        self.client.get('/admin/')
        self.client.get('/edit/')
        response = self.client.get('/spy/')
        self.assertIn('/admin/', response.content)
        self.assertIn('/edit/', response.content)

    def test_last_ten_request(self):
        """
        Ckeking number of request entrys in page context, also cheking
        url_path of this entrys with last ten visited pages.
        """
        urls = ['/spy/', '/', '/admin/', '/edit/', '/spy/', '/', '/admin/',
                '/edit/', '/']
        for i in urls:
            self.client.get(i)
        responce = self.client.get('/spy/')
        self.assertEqual(len(responce.context['last_requests']), 10)
        urls.append('/spy/')
        urls.reverse()
        index = 0
        for i in responce.context['last_requests']:
            self.assertEquals(i.url_path, urls[index])
            index += 1


class AuthTester(TestCase):

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


class EditorTester(TestCase):

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
        sergii = Contact.objects.all()[0]
        sergii.first_name = 'Andrii'
        sergii.save()
        responce = self.client.get('/edit/')
        self.assertIn('Andrii', responce.content)

    def test_editor_without_andrii(self):
        """
        Testing edit page.
        """
        Contact.objects.all().delete()
        create_other_user()
        responce = self.client.get('/edit/')
        self.assertIn('Andrii', responce.content)

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
        self.client.get('/')
        middle = RequestEntry.objects.all()[0]
        url = re.search("href=(\S+)>", admin_editor_url(middle)).group(1)
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, 200)


def create_other_user():
        Contact.objects.create(first_name='Andrii', last_name='Vanzha',
                               email='andrii@mail.ru',
                               contacts='+380662453012',
                               bio='His little story!')



