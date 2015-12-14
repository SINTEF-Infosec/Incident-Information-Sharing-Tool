# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0035_auto_20150828_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='tlp_scheme',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='tlp_value',
        ),
        migrations.AddField(
            model_name='incident',
            name='tlp',
            field=models.TextField(default='{"scheme": "enisa", "value": "green", "fields": []}'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='provider',
            field=models.ForeignKey(default='e08043c6-af04-455a-8d93-6bb66565e67f', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='incidenttype',
            name='provider',
            field=models.ForeignKey(default='e08043c6-af04-455a-8d93-6bb66565e67f', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='liaison',
            name='provider',
            field=models.ForeignKey(default='e08043c6-af04-455a-8d93-6bb66565e67f', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='provider',
            field=models.ForeignKey(default='e08043c6-af04-455a-8d93-6bb66565e67f', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='provider',
            field=models.ForeignKey(default='e08043c6-af04-455a-8d93-6bb66565e67f', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='provider',
            field=models.ForeignKey(related_name='provides_subscriptions', default='e08043c6-af04-455a-8d93-6bb66565e67f', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='triggertype',
            name='provider',
            field=models.ForeignKey(default='e08043c6-af04-455a-8d93-6bb66565e67f', to='incidents.Entity'),
        ),
    ]
