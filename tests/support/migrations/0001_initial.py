# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arm_sections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Common',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
                ('pub_status', models.CharField(max_length=1, choices=[(b'D', b'Draft'), (b'P', b'Published')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('common_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='support.Common')),
                ('summary', models.TextField(default=b'Default', blank=True)),
            ],
            options={
            },
            bases=('support.common',),
        ),
        migrations.CreateModel(
            name='ComplexCommon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ComplexArticle',
            fields=[
                ('complexcommon_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='support.ComplexCommon')),
                ('summary', models.TextField(default=b'Default', blank=True)),
            ],
            options={
            },
            bases=('support.complexcommon',),
        ),
        migrations.CreateModel(
            name='CustomSection',
            fields=[
                ('section_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='arm_sections.Section')),
            ],
            options={
            },
            bases=('arm_sections.section',),
        ),
        migrations.CreateModel(
            name='MultipleManyToManyModel',
            fields=[
                ('complexcommon_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='support.ComplexCommon')),
                ('more_sections', models.ManyToManyField(related_name=b'moresections_set', to='arm_sections.Section')),
            ],
            options={
            },
            bases=('support.complexcommon',),
        ),
        migrations.CreateModel(
            name='NonStandardField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('slugs_by_another_name', models.SlugField()),
                ('sections_by_another_name', models.ForeignKey(to='arm_sections.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionForeignKeyCommon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionForeignKeyArticle',
            fields=[
                ('sectionforeignkeycommon_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='support.SectionForeignKeyCommon')),
                ('summary', models.TextField(default=b'Default', blank=True)),
            ],
            options={
            },
            bases=('support.sectionforeignkeycommon',),
        ),
        migrations.CreateModel(
            name='SimpleCommon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimpleArticle',
            fields=[
                ('simplecommon_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='support.SimpleCommon')),
                ('summary', models.TextField(default=b'Default', blank=True)),
            ],
            options={
            },
            bases=('support.simplecommon',),
        ),
        migrations.AddField(
            model_name='simplecommon',
            name='primary_section',
            field=models.ForeignKey(to='arm_sections.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sectionforeignkeycommon',
            name='primary_section',
            field=models.ForeignKey(to='arm_sections.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complexcommon',
            name='primary_section',
            field=models.ForeignKey(to='arm_sections.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complexcommon',
            name='related_sections',
            field=models.ManyToManyField(related_name=b'relatedcomplexcommon_set', to='arm_sections.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='common',
            name='sections',
            field=models.ManyToManyField(to='arm_sections.Section'),
            preserve_default=True,
        ),
    ]
