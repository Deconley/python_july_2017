# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-24 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_secrets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='_user_friends_+', to='dojo_secrets.User'),
        ),
    ]