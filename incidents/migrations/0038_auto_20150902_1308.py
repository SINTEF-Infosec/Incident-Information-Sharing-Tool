# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0037_auto_20150901_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='tlp',
            field=models.ForeignKey(to='incidents.TLP', null=True, related_name='incident'),
        ),
        migrations.AlterField(
            model_name='tlp',
            name='schema',
            field=models.CharField(choices=[('us-cert', 'US-CERT'), ('enisa', 'ENISA')], max_length=15, default='enisa'),
        ),
        migrations.AlterField(
            model_name='tlp',
            name='value',
            field=models.CharField(choices=[('red', 'RED'), ('amber', 'AMBER'), ('green', 'GREEN'), ('white', 'WHITE')], max_length=5, default='amber'),
        ),
        migrations.AlterField(
            model_name='tlpfield',
            name='schema',
            field=models.CharField(choices=[('us-cert', 'US-CERT'), ('enisa', 'ENISA')], max_length=15, default='enisa'),
        ),
        migrations.AlterField(
            model_name='tlpfield',
            name='value',
            field=models.CharField(choices=[('red', 'RED'), ('amber', 'AMBER'), ('green', 'GREEN'), ('white', 'WHITE')], max_length=5, default='amber'),
        ),
    ]
