# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0015_auto_20150409_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.ForeignKey(to='incidents.NotificationType', null=True),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='notification_type',
            field=models.ForeignKey(to='incidents.NotificationType', related_name='incidents'),
        ),
    ]
