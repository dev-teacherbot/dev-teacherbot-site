# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_auto_20161024_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cbot',
            name='aiml_config',
            field=models.ManyToManyField(related_name='mlconfig', verbose_name=b'Active Chatbot Setups', to='chatbot.aiml_config', blank=True),
        ),
        migrations.AlterField(
            model_name='cbot',
            name='pandora_name',
            field=models.CharField(default=b'teacherbotlive', unique=True, max_length=70),
        ),
    ]
