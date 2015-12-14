# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationincident',
            name='triggers',
        ),
        migrations.AddField(
            model_name='notificationtrigger',
            name='notification_incident',
            field=models.ForeignKey(to='incidents.NotificationIncident'),
            preserve_default=False,
        ),
    ]
