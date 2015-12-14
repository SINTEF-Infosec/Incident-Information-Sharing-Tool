# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0027_auto_20150807_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnduserNotification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('message', models.TextField()),
                ('users', models.TextField()),
                ('resources', models.TextField()),
                ('incident', models.ForeignKey(to='incidents.Incident')),
            ],
        ),
    ]
