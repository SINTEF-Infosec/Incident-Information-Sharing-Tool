# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0014_auto_20150409_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationincident',
            name='notification_type',
            field=models.ForeignKey(to='incidents.NotificationType', related_name='incidents', null=True),
        ),
    ]
