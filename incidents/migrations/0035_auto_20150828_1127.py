# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0034_auto_20150819_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='tlp_scheme',
            field=models.CharField(max_length=255, default='enisa'),
        ),
        migrations.AddField(
            model_name='incident',
            name='tlp_value',
            field=models.CharField(max_length=5, default='green'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='4abe30d5-1f11-4e95-a62f-62cb1e2ad232'),
        ),
        migrations.AlterField(
            model_name='incidenttype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='4abe30d5-1f11-4e95-a62f-62cb1e2ad232'),
        ),
        migrations.AlterField(
            model_name='liaison',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='4abe30d5-1f11-4e95-a62f-62cb1e2ad232'),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='4abe30d5-1f11-4e95-a62f-62cb1e2ad232'),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='4abe30d5-1f11-4e95-a62f-62cb1e2ad232'),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='4abe30d5-1f11-4e95-a62f-62cb1e2ad232', related_name='provides_subscriptions'),
        ),
        migrations.AlterField(
            model_name='triggertype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='4abe30d5-1f11-4e95-a62f-62cb1e2ad232'),
        ),
    ]
