# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0040_remove_tlpfield_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='next_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='0fad2538-35cc-48c9-86fb-ee5332fcf767'),
        ),
        migrations.AlterField(
            model_name='incidenttype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='0fad2538-35cc-48c9-86fb-ee5332fcf767'),
        ),
        migrations.AlterField(
            model_name='liaison',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='0fad2538-35cc-48c9-86fb-ee5332fcf767'),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='0fad2538-35cc-48c9-86fb-ee5332fcf767'),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='0fad2538-35cc-48c9-86fb-ee5332fcf767'),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='0fad2538-35cc-48c9-86fb-ee5332fcf767', related_name='provides_subscriptions'),
        ),
        migrations.AlterField(
            model_name='triggertype',
            name='provider',
            field=models.ForeignKey(to='incidents.Entity', default='0fad2538-35cc-48c9-86fb-ee5332fcf767'),
        ),
    ]
