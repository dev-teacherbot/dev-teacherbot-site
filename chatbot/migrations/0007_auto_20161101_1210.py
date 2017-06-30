# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import chatbot.models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0006_auto_20161026_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiml_file',
            name='content',
            field=tinymce.models.HTMLField(default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aiml_config',
            name='aiml_files',
            field=models.ManyToManyField(related_name='AIML_File', verbose_name=b'Current Setup Files', to='chatbot.aiml_file', blank=True),
        ),
        migrations.AlterField(
            model_name='aiml_file',
            name='docfile',
            field=models.FileField(upload_to=chatbot.models.get_upload_directory),
        ),
    ]
