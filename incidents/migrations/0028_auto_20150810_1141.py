# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0027_auto_20150807_1018'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customfieldvalue',
            unique_together=set([('id', 'incident')]),
        ),
    ]
