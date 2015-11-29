# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2015-11-28 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=32, verbose_name='phone')),
                ('status', models.CharField(choices=[('ok', 'ok'), ('error', 'error'), ('pending', 'pending')], default='pending', max_length=32, verbose_name='status')),
                ('message', models.CharField(help_text='message by origin', max_length=128, verbose_name='message')),
                ('payload', models.TextField(blank=True, verbose_name='provider payload')),
                ('level', models.PositiveIntegerField(default=10, help_text="logger's level", verbose_name='level')),
            ],
            options={
                'verbose_name_plural': 'SMS logs',
                'verbose_name': 'SMS Log',
            },
        ),
    ]
