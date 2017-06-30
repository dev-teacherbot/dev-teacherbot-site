# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0008_remove_aiml_file_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aiml_file',
            name='text_file',
            field=models.TextField(default=b'', verbose_name=b'File Contents', blank=True),
        ),
        migrations.AlterField(
            model_name='cbot',
            name='pandora_name',
            field=models.CharField(default=b'', unique=True, max_length=70),
        ),
    ]
