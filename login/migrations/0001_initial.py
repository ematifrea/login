# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'login_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('password', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'login', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'login_user')


    models = {
        u'login.user': {
            'Meta': {'object_name': 'User'},
            'account_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login_date': ('django.db.models.fields.DateTimeField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['login']