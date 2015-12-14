# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0018_customfield_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customfieldvalue',
            unique_together=set([('type', 'incident')]),
        ),
    ]
