# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('format', models.CharField(max_length=255, choices=[('iodef', 'IODEF'), ('imdef', 'IMDEF'), ('cybox', 'CybOX'), ('zip', 'ZIP'), ('tar', 'TAR')])),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=6, choices=[('string', 'String'), ('int', 'Integer'), ('bool', 'Boolean')])),
            ],
        ),
        migrations.CreateModel(
            name='CustomFieldValue',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('language', models.CharField(max_length=5)),
                ('status', models.CharField(max_length=10, choices=[('resolved', 'Resolved'), ('unresolved', 'Unresolved')])),
                ('impact', models.CharField(max_length=6, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')])),
                ('summary', models.TextField()),
                ('description', models.TextField()),
                ('occurrence_time', models.DateTimeField()),
                ('detection_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='IncidentType',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('consequence', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Liaison',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=19)),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('generation_time', models.DateTimeField()),
                ('sent', models.DateTimeField()),
                ('sender', models.CharField(max_length=255)),
                ('hmac', models.CharField(max_length=255)),
                ('incidents', models.ManyToManyField(to='incidents.Incident')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationIncident',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationTrigger',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('method', models.CharField(max_length=255, choices=[('and', 'AND'), ('or', 'OR'), ('none', 'NONE')])),
                ('threshold', models.FloatField()),
                ('comparator', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('endpoint', models.URLField()),
                ('incidents', models.ManyToManyField(to='incidents.NotificationIncident')),
            ],
        ),
        migrations.CreateModel(
            name='TriggerType',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('threshold_type', models.CharField(max_length=255)),
                ('comparators', models.CharField(max_length=255)),
                ('incident_type', models.ForeignKey(to='incidents.IncidentType')),
            ],
        ),
        migrations.AddField(
            model_name='notificationtrigger',
            name='type',
            field=models.ForeignKey(to='incidents.TriggerType'),
        ),
        migrations.AddField(
            model_name='notificationincident',
            name='triggers',
            field=models.ManyToManyField(to='incidents.NotificationTrigger'),
        ),
        migrations.AddField(
            model_name='notificationincident',
            name='type',
            field=models.ForeignKey(to='incidents.IncidentType'),
        ),
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.ForeignKey(to='incidents.NotificationType'),
        ),
        migrations.AddField(
            model_name='incident',
            name='liaison',
            field=models.ForeignKey(to='incidents.Liaison'),
        ),
        migrations.AddField(
            model_name='incident',
            name='parent',
            field=models.ForeignKey(to='incidents.Incident'),
        ),
        migrations.AddField(
            model_name='incident',
            name='type',
            field=models.ForeignKey(to='incidents.IncidentType'),
        ),
        migrations.AddField(
            model_name='customfieldvalue',
            name='incident',
            field=models.ForeignKey(to='incidents.Incident'),
        ),
        migrations.AddField(
            model_name='customfieldvalue',
            name='type',
            field=models.ForeignKey(to='incidents.CustomField'),
        ),
        migrations.AddField(
            model_name='customfield',
            name='incident_type',
            field=models.ForeignKey(to='incidents.IncidentType'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='incident',
            field=models.ForeignKey(to='incidents.Incident'),
        ),
    ]
