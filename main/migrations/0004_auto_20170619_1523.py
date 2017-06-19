# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_pricedifference_data_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricedifference',
            old_name='ctiem',
            new_name='ctime',
        ),
        migrations.AlterField(
            model_name='pricedifference',
            name='data_type',
            field=models.IntegerField(choices=[(2, 'ETH/BTC'), (1, 'LTC/BTC'), (3, 'ETH/LTC')], verbose_name='数据类型'),
        ),
    ]
