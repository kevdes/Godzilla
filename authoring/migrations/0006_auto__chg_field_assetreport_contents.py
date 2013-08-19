# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AssetReport.contents'
        db.alter_column(u'authoring_assetreport', 'contents', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'AssetReport.contents'
        db.alter_column(u'authoring_assetreport', 'contents', self.gf('django.db.models.fields.TextField')(default=''))

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
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.AssetReport']", 'null': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.AssetReportStatus']"}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'work_order': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'authoring.assetreportstatus': {
            'Meta': {'object_name': 'AssetReportStatus'},
            'asset_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authoring.AssetType']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'finalised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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