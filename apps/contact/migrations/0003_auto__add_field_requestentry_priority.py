# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RequestEntry.priority'
        db.add_column(u'contact_requestentry', 'priority',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RequestEntry.priority'
        db.delete_column(u'contact_requestentry', 'priority')


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
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
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