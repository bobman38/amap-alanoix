# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20160615_0824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('deliverydate', models.ForeignKey(to='delivery.DeliveryDate')),
                ('product', models.ForeignKey(to='delivery.Product')),
            ],
        ),
    ]
