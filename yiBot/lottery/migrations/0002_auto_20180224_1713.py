# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-24 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winningnumbers',
            name='specialNum',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
