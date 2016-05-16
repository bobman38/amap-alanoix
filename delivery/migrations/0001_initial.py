# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


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
                ('date_min', models.DateField(null=True)),
                ('date_max', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True, verbose_name=b'Date de Livraison')),
                ('comment', models.CharField(max_length=500, null=True, blank=True)),
                ('ref_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateField(default=datetime.datetime.now, verbose_name=b'Date de Creation')),
                ('leave_date', models.DateField(null=True, verbose_name=b'Date de d\xc3\xa9part', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField()),
                ('comment', models.CharField(max_length=500, null=True, blank=True)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('contract', models.ForeignKey(to='delivery.Contract')),
                ('family', models.ForeignKey(to='delivery.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('date', models.ForeignKey(to='delivery.DeliveryDate')),
                ('member', models.ForeignKey(related_name='orders', to='delivery.Membership')),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('short_product_name', models.CharField(max_length=5)),
                ('description', models.TextField(null=True, blank=True)),
                ('mail', models.EmailField(max_length=254, null=True, blank=True)),
                ('tel', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=500, null=True, blank=True)),
                ('web', models.URLField(null=True, blank=True)),
                ('ref_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('unit_price', models.FloatField()),
                ('producer', models.ForeignKey(related_name='products', to='delivery.Producer')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tel', models.CharField(max_length=100, null=True, blank=True)),
                ('family', models.ForeignKey(related_name='users', blank=True, to='delivery.Family', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
            field=models.ManyToManyField(related_name='contracts', to='delivery.DeliveryDate'),
        ),
        migrations.AddField(
            model_name='contract',
            name='members',
            field=models.ManyToManyField(to='delivery.Family', through='delivery.Membership'),
        ),
        migrations.AddField(
            model_name='contract',
            name='producer',
            field=models.ForeignKey(to='delivery.Producer'),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('member', 'product', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('family', 'contract')]),
        ),
    ]
