# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20150915_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='short_product_name',
            field=models.CharField(default='O', max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contract',
            name='dates',
            field=models.ManyToManyField(related_name='contracts', to='delivery.DeliveryDate'),
        ),
    ]
