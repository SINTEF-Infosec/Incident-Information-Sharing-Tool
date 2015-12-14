# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0007_auto_20150320_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationtype',
            name='subscriber',
            field=models.ForeignKey(to='incidents.Subscriber', default='7e9fc912-1624-4d91-a7d4-4b536a41dbf1'),
            preserve_default=False,
        ),
    ]
