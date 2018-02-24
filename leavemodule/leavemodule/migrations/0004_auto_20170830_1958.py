# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leavemodule', '0003_auto_20170830_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='id',
        ),
        migrations.AddField(
            model_name='leave',
            name='leave_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leave',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]