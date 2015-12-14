# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0006_auto_20150320_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='subscriber',
        ),
        migrations.AddField(
            model_name='subscriber',
            name='notes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
