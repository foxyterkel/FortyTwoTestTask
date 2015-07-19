# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import apps.contact.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('birth_date', models.DateField(default=django.utils.timezone.now)),
                ('contacts', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(b'[+]\\d{12}')])),
                ('bio', models.TextField(max_length=250, validators=[django.core.validators.MinLengthValidator(10)])),
                ('email', models.EmailField(unique=True, max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('jaber', models.CharField(default=b'example@mail.ru', unique=True, max_length=100, blank=True)),
                ('skype', models.CharField(default=b'example', unique=True, max_length=100, blank=True)),
                ('other_contacts', models.TextField(max_length=250, blank=True)),
                ('photo', models.ImageField(upload_to=apps.contact.models.generate_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyMiddle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=250)),
                ('watched', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
