# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 21:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icebreaker_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blocked',
            field=models.ManyToManyField(blank=True, null=True, to='icebreaker_backend.Blocked'),
        ),
        migrations.AlterField(
            model_name='user',
            name='contacts',
            field=models.ManyToManyField(blank=True, null=True, to='icebreaker_backend.Contacts'),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icebreaker_backend.Picture'),
        ),
    ]
