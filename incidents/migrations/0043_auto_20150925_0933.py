# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0042_auto_20150923_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='endpoint',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='parent',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='provider',
            field=models.ForeignKey(default='84e847f929d34f66a94bf376cf30d12c', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='incidenttype',
            name='provider',
            field=models.ForeignKey(default='84e847f929d34f66a94bf376cf30d12c', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='liaison',
            name='provider',
            field=models.ForeignKey(default='84e847f929d34f66a94bf376cf30d12c', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='provider',
            field=models.ForeignKey(default='84e847f929d34f66a94bf376cf30d12c', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='provider',
            field=models.ForeignKey(default='84e847f929d34f66a94bf376cf30d12c', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='84e847f929d34f66a94bf376cf30d12c', related_name='provides_subscriptions'),
        ),
        migrations.AlterField(
            model_name='triggertype',
            name='provider',
            field=models.ForeignKey(default='84e847f929d34f66a94bf376cf30d12c', to='incidents.Entity'),
        ),
    ]
