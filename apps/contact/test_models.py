from django.test import TestCase

from apps.contact.models import Contact, RequestEntry, Signal


class MainTesterModels(TestCase):

    def test_main(self):
        """
        test_main for testing entry in base.
        """
        contact = Contact.objects.all()
        self.assertEqual(len(contact), 1)
        self.assertEqual(contact[0].first_name, 'Sergii')


class SpyTesterModels(TestCase):

    def test_request_spy_for_creating(self):
        """
        Checking status code of the page, and increasing number of the
        models entry after visiting 1 link.
        """
        first_watched = len(RequestEntry.objects.filter(watched=False))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        secound_watched = RequestEntry.objects.filter(watched=False)
        self.assertEqual(len(secound_watched), first_watched+1)


class SignalTester(TestCase):

    def test_signal_create(self):
        """
        testing signal create.
        """
        create_other_user()
        count = len(Signal.objects.all())
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
        sergii = Contact.objects.all()[0]
        sergii.first_name = 'Andrii'
        sergii.save()
        latest = Signal.objects.last()
        self.assertEqual(latest.action, 'save')


def create_other_user():
        Contact.objects.create(first_name='Andrii', last_name='Vanzha',
                               email='andrii@mail.ru',
                               contacts='+380662453012',
                               bio='His little story!')
