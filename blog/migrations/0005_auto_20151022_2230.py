# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20151022_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 22, 30, 3, 257058)),
        ),
    ]
