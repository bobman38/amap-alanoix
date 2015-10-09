# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_auto_20151001_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='web',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='mail',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
