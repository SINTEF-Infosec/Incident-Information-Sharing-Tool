# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0016_auto_20150409_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='provider',
            field=models.ForeignKey(to='incidents.Provider', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AddField(
            model_name='incidenttype',
            name='provider',
            field=models.ForeignKey(to='incidents.Provider', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AddField(
            model_name='liaison',
            name='provider',
            field=models.ForeignKey(to='incidents.Provider', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AddField(
            model_name='notificationincident',
            name='provider',
            field=models.ForeignKey(to='incidents.Provider', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AddField(
            model_name='notificationtrigger',
            name='provider',
            field=models.ForeignKey(to='incidents.Provider', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AddField(
            model_name='notificationtype',
            name='provider',
            field=models.ForeignKey(to='incidents.Provider', default='452a77a5414a49d3860b23dd3a563967'),
        ),
        migrations.AddField(
            model_name='triggertype',
            name='provider',
            field=models.ForeignKey(to='incidents.Provider', default='452a77a5414a49d3860b23dd3a563967'),
        ),
    ]
