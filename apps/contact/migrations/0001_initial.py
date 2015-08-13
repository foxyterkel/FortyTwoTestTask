# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table(u'contact_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('contacts', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('jaber', self.gf('django.db.models.fields.CharField')(default='example@mail.ru', max_length=100, blank=True)),
            ('skype', self.gf('django.db.models.fields.CharField')(default='example', max_length=100, blank=True)),
            ('other_contacts', self.gf('django.db.models.fields.TextField')(max_length=250, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'contact', ['Contact'])

        # Adding model 'RequestEntry'
        db.create_table(u'contact_requestentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('watched', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'contact', ['RequestEntry'])

        # Adding model 'Signal'
        db.create_table(u'contact_signal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('time', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'contact', ['Signal'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table(u'contact_contact')

        # Deleting model 'RequestEntry'
        db.delete_table(u'contact_requestentry')

        # Deleting model 'Signal'
        db.delete_table(u'contact_signal')


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