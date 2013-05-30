# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Color'
        db.create_table(u'plants_color', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'plants', ['Color'])

        # Adding M2M table for field m_flower_color on 'Plant'
        db.create_table(u'plants_plant_m_flower_color', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('plant', models.ForeignKey(orm[u'plants.plant'], null=False)),
            ('color', models.ForeignKey(orm[u'plants.color'], null=False))
        ))
        db.create_unique(u'plants_plant_m_flower_color', ['plant_id', 'color_id'])

        # Adding M2M table for field m_leaf_color on 'Plant'
        db.create_table(u'plants_plant_m_leaf_color', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('plant', models.ForeignKey(orm[u'plants.plant'], null=False)),
            ('color', models.ForeignKey(orm[u'plants.color'], null=False))
        ))
        db.create_unique(u'plants_plant_m_leaf_color', ['plant_id', 'color_id'])


    def backwards(self, orm):
        # Deleting model 'Color'
        db.delete_table(u'plants_color')

        # Removing M2M table for field m_flower_color on 'Plant'
        db.delete_table('plants_plant_m_flower_color')

        # Removing M2M table for field m_leaf_color on 'Plant'
        db.delete_table('plants_plant_m_leaf_color')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'plants.category': {
            'Meta': {'ordering': "('category',)", 'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'plants.color': {
            'Meta': {'ordering': "('color',)", 'object_name': 'Color'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'plants.commonname': {
            'Meta': {'object_name': 'CommonName'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plants.Plant']"})
        },
        u'plants.cultivar': {
            'Meta': {'object_name': 'Cultivar'},
            'cultivar': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plants.Plant']"})
        },
        u'plants.oldurl': {
            'Meta': {'object_name': 'OldUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_url': ('django.db.models.fields.URLField', [], {'max_length': '128', 'null': 'True'}),
            'plant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plants.Plant']"})
        },
        u'plants.plant': {
            'Meta': {'object_name': 'Plant'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['plants.Category']", 'symmetrical': 'False'}),
            'climbing_method': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'depth': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'distribution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'drought_tolerant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edibility': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'exposure': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'flower': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'flower_color': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'flowering_period': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'foliage': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'found': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'fragrance': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'fronds': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'fruit': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'growth_rate': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'habit': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'hardiness': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inflorescence': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'internal_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'leaf': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'life_cycle': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'light': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'm_flower_color': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'plant_flower_color'", 'symmetrical': 'False', 'to': u"orm['plants.Color']"}),
            'm_leaf_color': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'plant_leaf_color'", 'symmetrical': 'False', 'to': u"orm['plants.Color']"}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'organ': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'poison_part': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'propagation': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'regions': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'season': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'severity': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'soil': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'space': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'storage': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sub_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'symptoms': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'texture': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'toxic_principle': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'update_by': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'usage': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'zones': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        u'plants.plantimage': {
            'Meta': {'object_name': 'PlantImage'},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'height': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'plant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plants.Plant']"}),
            'thumbnail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'width': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['plants']