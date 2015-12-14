# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0003_auto_20150317_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationincident',
            name='name',
            field=models.CharField(default='Placeholder', max_length=255),
            preserve_default=False,
        ),
    ]
