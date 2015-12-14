# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0010_auto_20150326_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='hmac',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
