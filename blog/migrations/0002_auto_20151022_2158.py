# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['creation_date']},
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['-publication_date'], 'verbose_name_plural': 'entries'},
        ),
        migrations.AddField(
            model_name='entry',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 22, 21, 58, 52, 208941)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(related_name='comments', to='blog.Entry'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='body',
            field=models.TextField(verbose_name=b'Contenu'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=255, verbose_name=b'Titre'),
        ),
    ]
