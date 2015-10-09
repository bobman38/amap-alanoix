# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0003_auto_20150915_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverydate',
            name='ref_user',
        ),
        migrations.AddField(
            model_name='deliverydate',
            name='ref_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
