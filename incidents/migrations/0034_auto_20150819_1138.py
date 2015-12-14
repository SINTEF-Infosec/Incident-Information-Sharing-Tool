# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.OAUTH2_PROVIDER_APPLICATION_MODEL),
        ('incidents', '0033_auto_20150819_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityOAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('application', models.OneToOneField(to=settings.OAUTH2_PROVIDER_APPLICATION_MODEL)),
                ('entity', models.OneToOneField(to='incidents.Entity')),
            ],
        ),
        migrations.AddField(
            model_name='oauthremoteclient',
            name='entity',
            field=models.OneToOneField(default='e31d50d0c5ed491b9e3bb6f580f37e70', to='incidents.Entity'),
            preserve_default=False,
        ),
    ]
