# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0010_auto_20151002_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField()),
                ('comment', models.CharField(max_length=500)),
                ('amount', models.FloatField()),
                ('contract', models.ForeignKey(to='delivery.Contract')),
                ('family', models.ForeignKey(to='delivery.Family')),
            ],
        ),
        migrations.AlterModelOptions(
            name='deliverydate',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='order',
            name='family',
            field=models.ForeignKey(related_name='orders', to='delivery.Family'),
        ),
        migrations.AddField(
            model_name='contract',
            name='members',
            field=models.ManyToManyField(to='delivery.Family', through='delivery.Membership'),
        ),
    ]
