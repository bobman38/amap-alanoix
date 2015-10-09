# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'Date de Livraison')),
                ('comment', models.CharField(max_length=500, null=True, blank=True)),
                ('ref_user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(verbose_name=b'Date de Creation')),
                ('leave_date', models.DateTimeField(null=True, verbose_name=b'Date de d\xc3\xa9part', blank=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('date', models.ForeignKey(to='delivery.DeliveryDate')),
                ('family', models.ForeignKey(to='delivery.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('mail', models.CharField(max_length=200, null=True, blank=True)),
                ('tel', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=500, null=True, blank=True)),
                ('ref_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('unit_price', models.FloatField()),
                ('producer', models.ForeignKey(to='delivery.Producer')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='delivery.Product'),
        ),
        migrations.AddField(
            model_name='contract',
            name='dates',
            field=models.ManyToManyField(to='delivery.DeliveryDate'),
        ),
        migrations.AddField(
            model_name='contract',
            name='producer',
            field=models.ForeignKey(to='delivery.Producer'),
        ),
    ]
