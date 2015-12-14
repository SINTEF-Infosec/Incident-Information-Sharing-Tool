# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0032_oauthremoteclient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentnotificationstatus',
            name='incident',
            field=models.OneToOneField(to='incidents.Incident'),
        ),
    ]
