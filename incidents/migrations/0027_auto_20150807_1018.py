# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0026_remove_triggertype_threshold_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='format',
            field=models.CharField(choices=[('iodef', 'IODEF'), ('imdef', 'IMDEF'), ('cybox', 'CybOX'), ('zip', 'ZIP'), ('tar', 'TAR'), ('csv', 'CSV')], max_length=255),
        ),
        migrations.AlterField(
            model_name='incident',
            name='impact',
            field=models.FloatField(choices=[(1.0, 'High'), (0.5, 'Medium'), (0.1, 'Low')]),
        ),
    ]
