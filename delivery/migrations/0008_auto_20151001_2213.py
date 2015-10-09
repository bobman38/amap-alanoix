# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_auto_20151001_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='date_max',
            field=models.DateField(default=datetime.datetime(2015, 10, 1, 20, 13, 21, 504503, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='date_min',
            field=models.DateField(default=datetime.datetime(2015, 10, 1, 20, 13, 29, 393638, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
