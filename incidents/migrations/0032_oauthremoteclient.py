# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0031_auto_20150819_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthRemoteClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token_endpoint', models.URLField()),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
            ],
        ),
    ]
