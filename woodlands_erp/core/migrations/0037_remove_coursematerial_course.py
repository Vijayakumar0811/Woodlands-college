# Generated by Django 5.2.4 on 2025-07-23 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_subject_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursematerial',
            name='course',
        ),
    ]
