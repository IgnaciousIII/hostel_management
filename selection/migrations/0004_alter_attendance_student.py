# Generated by Django 5.1.7 on 2025-03-31 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0003_rename_name_visitor_visitor_name_visitor_warden_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selection.student'),
        ),
    ]
