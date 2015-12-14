# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0019_auto_20150417_1507'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customfieldvalue',
            unique_together=set([]),
        ),
    ]
