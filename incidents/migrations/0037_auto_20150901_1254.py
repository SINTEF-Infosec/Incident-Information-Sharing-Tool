# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0036_auto_20150828_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='TLP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('schema', models.CharField(max_length=15, choices=[('us-cert', 'US-CERT'), ('enisa', 'ENISA')])),
                ('value', models.CharField(max_length=5, choices=[('red', 'RED'), ('amber', 'AMBER'), ('green', 'GREEN'), ('white', 'WHITE')])),
            ],
        ),
        migrations.CreateModel(
            name='TLPField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('field', models.CharField(max_length=255)),
                ('schema', models.CharField(max_length=15, choices=[('us-cert', 'US-CERT'), ('enisa', 'ENISA')])),
                ('value', models.CharField(max_length=5, choices=[('red', 'RED'), ('amber', 'AMBER'), ('green', 'GREEN'), ('white', 'WHITE')])),
                ('tlp', models.ForeignKey(to='incidents.TLP')),
            ],
        ),
        migrations.AlterField(
            model_name='incident',
            name='tlp',
            field=models.ForeignKey(to='incidents.TLP', null=True),
        ),
    ]
