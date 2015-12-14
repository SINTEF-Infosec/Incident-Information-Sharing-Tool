# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0020_auto_20150417_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(null=True, blank=True, upload_to=''),
        ),
    ]
