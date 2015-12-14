# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0029_auto_20150810_1145'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customfieldvalue',
            unique_together=set([('incident', 'type')]),
        ),
    ]
