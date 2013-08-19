# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AssetReportStatus'
        db.create_table(u'authoring_assetreportstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('finalised', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'authoring', ['AssetReportStatus'])

        # Adding model 'AssetReport'
        db.create_table(u'authoring_assetreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authoring.Asset'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authoring.AssetReportStatus'])),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('work_order', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('response_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authoring.AssetReport'])),
            ('submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'authoring', ['AssetReport'])


    def backwards(self, orm):
        # Deleting model 'AssetReportStatus'
        db.delete_table(u'authoring_assetreportstatus')

        # Deleting model 'AssetReport'
        db.delete_table(u'authoring_assetreport')


    models = {
        u'authoring.asset': {
            'Meta': {'object_name': 'Asset'},
            'asset_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.AssetType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['management.Product']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.AssetStatus']"})
        },
        u'authoring.assetreport': {
            'Meta': {'ordering': "('date_created',)", 'object_name': 'AssetReport'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.Asset']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.AssetReport']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.AssetReportStatus']"}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_order': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'authoring.assetreportstatus': {
            'Meta': {'object_name': 'AssetReportStatus'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'finalised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'authoring.assetstatus': {
            'Meta': {'object_name': 'AssetStatus'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'finalised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'authoring.assettype': {
            'Meta': {'ordering': "('display_order',)", 'object_name': 'AssetType'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
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

    complete_apps = ['authoring']