# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0013_auto_20150408_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='customfield',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='customfieldvalue',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='incident',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='incidenttype',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='liaison',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='notification',
            name='hmac',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='triggertype',
            name='id',
            field=models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4),
        ),
    ]
