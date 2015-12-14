# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0028_auto_20150810_1141'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customfieldvalue',
            unique_together=set([('id', 'incident', 'type')]),
        ),
    ]
