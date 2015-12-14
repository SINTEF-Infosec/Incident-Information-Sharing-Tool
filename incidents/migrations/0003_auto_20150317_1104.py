# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0002_auto_20150317_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationtype',
            name='incidents',
        ),
        migrations.AddField(
            model_name='notificationincident',
            name='notification_type',
            field=models.ForeignKey(to='incidents.NotificationType', default=1),
            preserve_default=False,
        ),
    ]
