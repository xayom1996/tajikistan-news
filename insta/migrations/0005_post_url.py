# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-05 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0004_auto_20180302_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.CharField(default='', max_length=100, verbose_name='Url'),
        ),
    ]