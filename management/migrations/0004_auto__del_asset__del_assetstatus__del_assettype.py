# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Asset'
        db.delete_table(u'management_asset')

        # Deleting model 'AssetStatus'
        db.delete_table(u'management_assetstatus')

        # Deleting model 'AssetType'
        db.delete_table(u'management_assettype')


    def backwards(self, orm):
        # Adding model 'Asset'
        db.create_table(u'management_asset', (
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['management.AssetStatus'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['management.Product'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('asset_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['management.AssetType'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'management', ['Asset'])

        # Adding model 'AssetStatus'
        db.create_table(u'management_assetstatus', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('finalised', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'management', ['AssetStatus'])

        # Adding model 'AssetType'
        db.create_table(u'management_assettype', (
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'management', ['AssetType'])


    models = {
        u'management.client': {
            'Meta': {'object_name': 'Client'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'management.product': {
            'Meta': {'object_name': 'Product'},
            'cat_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'finalised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['management']