# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0023_alert_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentNotificationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('notified', models.BooleanField(default=False)),
                ('incident', models.ForeignKey(to='incidents.Incident')),
            ],
        ),
    ]
