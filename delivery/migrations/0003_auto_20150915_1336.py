# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_auto_20150915_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydate',
            name='date',
            field=models.DateField(verbose_name=b'Date de Livraison'),
        ),
        migrations.AlterField(
            model_name='family',
            name='create_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Date de Creation'),
        ),
        migrations.AlterField(
            model_name='family',
            name='leave_date',
            field=models.DateField(null=True, verbose_name=b'Date de d\xc3\xa9part', blank=True),
        ),
    ]
