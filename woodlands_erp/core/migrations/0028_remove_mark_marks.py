# Generated by Django 5.2.4 on 2025-07-22 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_mark_exam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='marks',
        ),
    ]
