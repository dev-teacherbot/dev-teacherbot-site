# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_auto_20161024_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aiml_file',
            name='docfile',
            field=models.FileField(upload_to=b'aiml_files'),
        ),
    ]
