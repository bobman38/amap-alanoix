# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0009_auto_20151001_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(related_name='products', to='delivery.Producer'),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('family', 'product', 'date')]),
        ),
    ]
