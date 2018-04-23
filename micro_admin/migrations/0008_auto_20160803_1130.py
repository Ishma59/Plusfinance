# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0007_auto_20160730_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, default='off', max_length=5)),
                ('lvl', models.IntegerField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='micro_admin.Menu')),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('branch_manager', 'Can manage all accounts under his/her branch.'), ('content_managing', 'Can add, edit, delete content.'))},
        ),
    ]
