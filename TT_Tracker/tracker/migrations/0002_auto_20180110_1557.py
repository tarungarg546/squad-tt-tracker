# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-10 10:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='user_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondplayers', to=settings.AUTH_USER_MODEL),
        ),
    ]
