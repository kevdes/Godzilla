# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'management_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal(u'management', ['Client'])

        # Adding model 'Title'
        db.create_table(u'management_title', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['management.Client'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'management', ['Title'])

        # Adding model 'ProductType'
        db.create_table(u'management_producttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'management', ['ProductType'])

        # Adding model 'ProductStatus'
        db.create_table(u'management_productstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'management', ['ProductStatus'])

        # Adding model 'Product'
        db.create_table(u'management_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['management.Title'])),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['management.ProductType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['management.ProductStatus'])),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('cat_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'management', ['Product'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'management_client')

        # Deleting model 'Title'
        db.delete_table(u'management_title')

        # Deleting model 'ProductType'
        db.delete_table(u'management_producttype')

        # Deleting model 'ProductStatus'
        db.delete_table(u'management_productstatus')

        # Deleting model 'Product'
        db.delete_table(u'management_product')


    models = {
        u'management.client': {
            'Meta': {'object_name': 'Client'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'management.product': {
            'Meta': {'object_name': 'Product'},
            'cat_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['management.ProductType']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['management.ProductStatus']"}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['management.Title']"})
        },
        u'management.productstatus': {
            'Meta': {'object_name': 'ProductStatus'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'management.producttype': {
            'Meta': {'object_name': 'ProductType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'management.title': {
            'Meta': {'object_name': 'Title'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['management.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['management']