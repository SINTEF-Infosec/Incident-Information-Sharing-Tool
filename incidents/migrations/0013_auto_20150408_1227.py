# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0012_auto_20150327_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='hmac',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
    ]
