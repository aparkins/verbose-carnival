# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 00:39
from __future__ import unicode_literals

from django.db import migrations, models


def forwards(apps, schema_editor):
    with schema_editor.connection.cursor() as db:
        db.execute("""
        ALTER TABLE "dip_platform_game" ADD COLUMN "current_turn" integer DEFAULT 0 NOT NULL;
        """)


def backwards(apps, schema_editor):
    with schema_editor.connection.cursor() as db:
        db.execute("""
        ALTER TABLE "dip_platform_game" DROP COLUMN "current_turn" CASCADE;
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('dip_platform', '0001'),
    ]

    state_operations = [
        migrations.AddField(
            model_name='game',
            name='current_turn',
            field=models.IntegerField(default=0),
        ),
    ]

    database_operations = [migrations.RunPython(forwards, reverse_code=backwards, atomic=False)]
    operations = [migrations.SeparateDatabaseAndState(database_operations=database_operations, state_operations=state_operations)]
