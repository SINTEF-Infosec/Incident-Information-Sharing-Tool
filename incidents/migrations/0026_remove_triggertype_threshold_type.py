# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0025_auto_20150421_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triggertype',
            name='threshold_type',
        ),
    ]
