# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_auto_20151001_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydate',
            name='date',
            field=models.DateField(unique=True, verbose_name=b'Date de Livraison'),
        ),
    ]
