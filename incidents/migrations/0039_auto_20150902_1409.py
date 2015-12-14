# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0038_auto_20150902_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlpfield',
            name='tlp',
            field=models.ForeignKey(to='incidents.TLP', related_name='fields'),
        ),
    ]
