# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-09-02 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import menu.models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20180902_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateTimeField(validators=[menu.models.valid_expiry_date]),
        ),
    ]
