# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0007_auto_20161101_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aiml_file',
            name='content',
        ),
    ]
