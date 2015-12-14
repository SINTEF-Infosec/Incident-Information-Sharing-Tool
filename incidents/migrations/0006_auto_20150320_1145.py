# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0005_auto_20150318_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, default=uuid.uuid4, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, default=uuid.uuid4, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('endpoint', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, default=uuid.uuid4, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='incident',
            name='language',
            field=models.CharField(choices=[('en_US', 'English - American'), ('nb_NO', 'Norwegian')], max_length=50),
        ),
        migrations.AlterField(
            model_name='incident',
            name='parent',
            field=models.ForeignKey(blank=True, to='incidents.Incident', null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='subscriber',
            field=models.OneToOneField(to='incidents.Subscriber'),
        ),
    ]
