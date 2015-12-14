# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0008_notificationtype_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='url',
            field=models.URLField(default='www.test.com'),
            preserve_default=False,
        ),
    ]
