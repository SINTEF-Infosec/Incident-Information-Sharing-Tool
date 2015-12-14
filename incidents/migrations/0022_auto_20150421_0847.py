# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incidents', '0021_auto_20150420_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True)),
                ('type', models.CharField(max_length=255, choices=[('new_incident', 'New Incident'), ('updated_incident', 'Updated Incident'), ('assigned_incident', 'Assigned Incident')])),
                ('alert', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AlertStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('alert', models.ForeignKey(to='incidents.Alert')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='attachment',
            name='incident',
            field=models.ForeignKey(related_name='attachments', blank=True, to='incidents.Incident'),
        ),
        migrations.AddField(
            model_name='alert',
            name='notified',
            field=models.ManyToManyField(through='incidents.AlertStatus', to=settings.AUTH_USER_MODEL),
        ),
    ]
