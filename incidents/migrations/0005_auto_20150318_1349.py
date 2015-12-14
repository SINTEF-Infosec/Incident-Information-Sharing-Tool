# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0004_notificationincident_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='incident',
            field=models.ForeignKey(to='incidents.Incident', related_name='attachments'),
        ),
        migrations.AlterField(
            model_name='customfieldvalue',
            name='incident',
            field=models.ForeignKey(to='incidents.Incident', related_name='custom_fields'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='parent',
            field=models.ForeignKey(to='incidents.Incident', null=True),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='notification_type',
            field=models.ForeignKey(to='incidents.NotificationType', related_name='incidents'),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='notification_incident',
            field=models.ForeignKey(to='incidents.NotificationIncident', related_name='triggers'),
        ),
    ]
