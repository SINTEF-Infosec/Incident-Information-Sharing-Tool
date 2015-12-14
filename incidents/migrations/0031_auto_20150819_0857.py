# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0030_auto_20150810_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('endpoint', models.URLField()),
                ('provider', models.BooleanField(default=True)),
                ('owner', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='incident',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AlterField(
            model_name='incidenttype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AlterField(
            model_name='liaison',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='provider',
            field=models.ForeignKey(related_name='provides_subscriptions', default='452a77a5414a49d3860b23dd3a563967', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='subscriber',
            field=models.ForeignKey(related_name='subscriptions', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='triggertype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.DeleteModel(
            name='Provider',
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
    ]
