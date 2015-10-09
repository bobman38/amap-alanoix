# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_auto_20151001_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_max',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_min',
            field=models.DateField(null=True),
        ),
    ]
