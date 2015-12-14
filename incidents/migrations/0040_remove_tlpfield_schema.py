# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0039_auto_20150902_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tlpfield',
            name='schema',
        ),
    ]
