# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit_price',
            field=models.FloatField(verbose_name=b'Prix unitaire par d\xc3\xa9faut. Peut \xc3\xaatre chang\xc3\xa9 pour chaque livraison.'),
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together=set([('product', 'deliverydate')]),
        ),
    ]
