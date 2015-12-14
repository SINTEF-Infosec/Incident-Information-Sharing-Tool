# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0041_auto_20150908_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='apple_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='provider',
            field=models.ForeignKey(default='dab0df0a-d33c-4688-a32c-90b5d1c08a44', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='incidenttype',
            name='provider',
            field=models.ForeignKey(default='dab0df0a-d33c-4688-a32c-90b5d1c08a44', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='liaison',
            name='provider',
            field=models.ForeignKey(default='dab0df0a-d33c-4688-a32c-90b5d1c08a44', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationincident',
            name='provider',
            field=models.ForeignKey(default='dab0df0a-d33c-4688-a32c-90b5d1c08a44', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationtrigger',
            name='provider',
            field=models.ForeignKey(default='dab0df0a-d33c-4688-a32c-90b5d1c08a44', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='notificationtype',
            name='provider',
            field=models.ForeignKey(related_name='provides_subscriptions', default='dab0df0a-d33c-4688-a32c-90b5d1c08a44', to='incidents.Entity'),
        ),
        migrations.AlterField(
            model_name='triggertype',
            name='provider',
            field=models.ForeignKey(default='dab0df0a-d33c-4688-a32c-90b5d1c08a44', to='incidents.Entity'),
        ),
    ]
