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
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_login_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'login', ['User'])

        # Adding model 'UserActivation'
        db.create_table(u'login_useractivation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['login.User'], unique=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('key_expiration', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 14, 0, 0))),
        ))
        db.send_create_signal(u'login', ['UserActivation'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'login_user')

        # Deleting model 'UserActivation'
        db.delete_table(u'login_useractivation')


    models = {
        u'login.user': {
            'Meta': {'object_name': 'User'},
            'account_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'login.useractivation': {
            'Meta': {'object_name': 'UserActivation'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_expiration': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 14, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['login.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['login']