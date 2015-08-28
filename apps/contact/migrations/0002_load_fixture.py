# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        call_command('loaddata', 'init_data.json')

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'contact.contact': {
            'Meta': {'object_name': 'Contact'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jaber': ('django.db.models.fields.CharField', [], {'default': "'example@mail.ru'", 'max_length': '100', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'default': "'example'", 'max_length': '100', 'blank': 'True'})
        },
        u'contact.requestentry': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'RequestEntry'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'watched': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'contact.signal': {
            'Meta': {'object_name': 'Signal'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'time': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['contact']
    symmetrical = True
