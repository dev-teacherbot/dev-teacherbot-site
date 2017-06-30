# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_auto_20161021_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cbot',
            name='chatbot_name',
        ),
        migrations.AlterField(
            model_name='cbot',
            name='twit_token_secret',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'Twitter Access Token Secret'),
        ),
    ]
