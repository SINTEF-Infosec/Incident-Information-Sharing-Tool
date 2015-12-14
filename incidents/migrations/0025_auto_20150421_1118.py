# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0024_incidentnotificationstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentnotificationstatus',
            name='incident',
            field=models.ForeignKey(unique=True, to='incidents.Incident'),
        ),
    ]
