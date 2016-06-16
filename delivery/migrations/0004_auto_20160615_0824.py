# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_auto_20160520_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='family',
            field=models.ForeignKey(related_name='members', to='delivery.Family'),
        ),
    ]
