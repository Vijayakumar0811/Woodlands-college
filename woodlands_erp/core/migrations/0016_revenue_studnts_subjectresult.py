# Generated by Django 5.2.4 on 2025-07-21 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_facultyattendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('source', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Studnts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_number', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
                ('grade', models.CharField(choices=[('O', 'Outstanding'), ('A+', 'Excellent'), ('A', 'Very Good'), ('B+', 'Good'), ('B', 'Average'), ('C', 'Pass'), ('F', 'Fail')], max_length=2)),
                ('marks', models.FloatField()),
                ('credits', models.PositiveIntegerField(default=4)),
                ('grade_point', models.FloatField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='core.studnts')),
            ],
        ),
    ]
