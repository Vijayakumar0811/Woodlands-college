# Generated by Django 5.2.4 on 2025-07-21 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_parent_address_parent_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='course',
        ),
        migrations.AddField(
            model_name='exam',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.department'),
        ),
        migrations.AddField(
            model_name='exam',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subject'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='exam',
            name='year',
            field=models.CharField(max_length=10),
        ),
    ]
