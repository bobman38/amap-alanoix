# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0011_auto_20151007_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='comment',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('family', 'contract')]),
        ),
    ]
