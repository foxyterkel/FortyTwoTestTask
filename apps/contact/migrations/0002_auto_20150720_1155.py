# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fill_contact(apps, schema_editor):
    contact = apps.get_model('contact', 'Contact')
    contact.objects.create(first_name='Sergii', last_name='Vanzha',
                           birth_date='1991-01-19', contacts='+380662352011',
                           bio='My little story.', email='terkel919@gmail.com',
                           jaber='example@42.cc', skype='example',
                           other_contacts='city Poltava. Parkova 1a st.')


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fill_contact),
    ]
