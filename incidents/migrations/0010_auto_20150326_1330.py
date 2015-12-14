# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0009_subscriber_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sent',
            field=models.DateTimeField(blank=True),
        ),
    ]
