# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0010_auto_20150326_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('send_at', models.DateTimeField()),
                ('attempt', models.IntegerField(default=0)),
                ('notification', models.ForeignKey(to='incidents.Notification')),
            ],
        ),
    ]
