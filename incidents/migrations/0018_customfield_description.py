# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0017_auto_20150414_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='customfield',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
