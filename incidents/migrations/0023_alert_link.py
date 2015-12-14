# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0022_auto_20150421_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='link',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
