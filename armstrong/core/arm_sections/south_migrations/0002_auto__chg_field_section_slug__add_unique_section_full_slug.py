# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Section.slug'
        db.alter_column('arm_sections_section', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=200))
        # Adding unique constraint on 'Section', fields ['full_slug']
        db.create_unique('arm_sections_section', ['full_slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Section', fields ['full_slug']
        db.delete_unique('arm_sections_section', ['full_slug'])


        # Changing field 'Section.slug'
        db.alter_column('arm_sections_section', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

    models = {
        'arm_sections.section': {
            'Meta': {'object_name': 'Section'},
            'full_slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['arm_sections.Section']", 'null': 'True', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['arm_sections']