# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Date de Creation'),
        ),
    ]
