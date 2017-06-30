# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_auto_20161021_0938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aiml_config',
            options={'verbose_name': 'Setup', 'verbose_name_plural': 'Setups'},
        ),
        migrations.AlterField(
            model_name='aiml_config',
            name='aiml_files',
            field=models.ManyToManyField(related_name='AIML_File', verbose_name=b'Chatbot Setups', to='chatbot.aiml_file', blank=True),
        ),
        migrations.AlterField(
            model_name='aiml_config',
            name='title',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='aiml_file',
            name='text_file',
            field=models.TextField(default=b'', verbose_name=b'Plaintext Content', blank=True),
        ),
    ]
