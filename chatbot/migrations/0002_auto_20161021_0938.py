# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aiml_config',
            name='public',
        ),
        migrations.AddField(
            model_name='aiml_config',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name=b'Should be public?'),
        ),
    ]
