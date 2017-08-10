# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 07:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('core', '0002_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='campsiteindexpage',
            name='meta_description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='campsiteindexpage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='campsiteindexpage',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='campsitepage',
            name='meta_description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='campsitepage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='campsitepage',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hutindexpage',
            name='meta_description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='hutindexpage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='hutindexpage',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hutpage',
            name='meta_description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='hutpage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='hutpage',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
