# -*- coding: utf-8 -*-
"""
Django unit test for project fortytwo_test_task
Making client and superuser in setUp
each test for differnt parts of project
can be start as separare test
"""

from django.test import TestCase
import re
import json

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
                                             response.content)
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

    def check_rendered_page_for_content(self, obj, fields, content):
        for i in fields:
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
        entry = RequestEntry.objects.get(url_path='/spy/')
        self.assertIn(entry, response.context['last_requests'])

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
        entry = RequestEntry.objects.get(url_path='/spy/')
        self.assertIn(entry, response.context['last_requests'])

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
        entry = RequestEntry.objects.get(url_path='/spy/')
        self.assertIn(entry, response.context['last_requests'])

    def test_request_spy_entry(self):
        """
        Cheking visited url_path on the page of spy.
        """
        entry1 = RequestEntry.objects.create(url_path='/admin/')
        entry2 = RequestEntry.objects.create(url_path='/edit/')
        response = self.client.get('/spy/')
        self.assertIn(entry1, response.context['last_requests'])
        self.assertIn(entry2, response.context['last_requests'])

    def test_last_ten_request(self):
        """
        Ckeking number of request entrys in page context, also cheking
        url_path of this entrys with last ten visited pages.
        """
        urls = ['/spy/', '/', '/admin/', '/edit/', '/spy/', '/', '/admin/',
                '/edit/', '/']
        for i in urls:
            RequestEntry.objects.create(url_path=i)
        responce = self.client.get('/spy/')
        last_ten = RequestEntry.objects.all()[:10]
        self.assertEqual(list(last_ten),
                         list(responce.context['last_requests']))

    def test_page_for_randered_context(self):
        """
        Check if page renders context
        """
        responce = self.client.get('/spy/')
        for i in responce.context['last_requests']:
            self.assertIn(i.url_path, responce.content)


class AuthTester(TestCase):

    def test_auth_pass(self):
        """
        Authentication test. With correct data.
        """
        response = self.client.post('/account/login/', {'username': 'admin',
                                                        'password': 'admin'})
        self.assertEqual(response.status_code, 302)

    def test_auth_fail(self):
        """
        Authentication test. With incorrect data.
        """
        response = self.client.post('/account/login/', {'username': 'admyn',
                                                        'password': 'admin'})
        self.assertEqual(response.status_code, 200)


class EditorTester(TestCase):

    def test_editor_with_sergii(self):
        """
        Checking instance in context, and looking for the name on tha page
        loaded from fixtures.
        """
        responce = self.client.get('/edit/')
        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce.context['form'], EditForm)
        self.assertIn('Sergii', responce.content)

    def test_editor_without_sergii(self):
        """
        Cheking 404 if there ara no contact.
        """
        Contact.objects.all().delete()
        responce = self.client.get('/edit/')
        self.assertIn('Page Not Found', responce.content)

    def test_editor_without_sergii_rename(self):
        """
        Looking for the manually changed name in rendered page.
        """
        sergii = Contact.objects.all()[0]
        sergii.first_name = 'Andrii'
        sergii.save()
        responce = self.client.get('/edit/')
        self.assertIn('Andrii', responce.content)

    def test_editor_without_andrii(self):
        """
        Looking for the name of new created contact on the rendered page.
        """
        Contact.objects.all().delete()
        create_other_user()
        responce = self.client.get('/edit/')
        self.assertIn('Andrii', responce.content)

    def test_admin_editor_contact(self):
        """
        Testing castom template tags. Passing Contact object to function.
        Fetching url. And cheking status code after getting responce
        for this url.
        """
        contact = Contact.objects.all()[0]
        url = re.search("href=(\S+)>", admin_editor_url(contact)).group(1)
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, 200)

    def test_admin_editor_middle(self):
        """
        Testing castom template tags. Passing RequestEntry object to function.
        Fetching url. And cheking status code after getting responce
        for this url.
        """
        middle = RequestEntry.objects.create(url_path='/edit/')
        url = re.search("href=(\S+)>", admin_editor_url(middle)).group(1)
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, 200)

    def test_for_ajax_request_correct(self):
        """
        Sending request with json data for editing page,
        and check model for this changes
        """
        data = instance_to_dict(Contact.objects.first())
        for i in data:
            if i['name'] == 'first_name':
                i['value'] = 'Andrii'
        data_j = json.dumps(data)
        responce = self.client.post('/edit/', data={'form': data_j,
                                    'image': 'null'})
        self.assertEqual(responce.content, 'Saved! Your model was updated.')
        self.assertEqual(Contact.objects.first().first_name, 'Andrii')

    def test_for_ajax_request_incorrect(self):
        """
        Sending request with incorrect json data for editing page,
        and check model for initial state, and looking error keywords
        in responce.
        """
        data = instance_to_dict(Contact.objects.first())
        for i in data:
            if i['name'] == 'first_name':
                i['value'] = 'A'
            elif i['name'] == 'contacts':
                i['value'] = '1'
        data_j = json.dumps(data)
        responce = self.client.post('/edit/', data={'form': data_j,
                                    'image': 'null'})
        self.assertIn("first_name", responce.content)
        self.assertIn("contacts", responce.content)
        self.assertEqual(Contact.objects.first().first_name, 'Sergii')


def create_other_user():
        Contact.objects.create(first_name='Andrii', last_name='Vanzha',
                               email='andrii@mail.ru',
                               contacts='+380662453012',
                               bio='His little story!')


def instance_to_dict(ins):
        res = []
        fields = ['first_name', 'last_name', 'email', 'contacts', 'bio',
                  'birth_date']
        for i in ins.__dict__:
            if i in fields:
                res.append({'name': str(i), 'value': str(ins.__dict__[i])})
        return res
