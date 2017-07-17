# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0009_auto_20161104_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='cbot',
            name='twit_capable',
            field=models.BooleanField(default=False, verbose_name=b'Is twitter capable?'),
        ),
    ]
