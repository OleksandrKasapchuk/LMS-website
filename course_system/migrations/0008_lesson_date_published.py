# Generated by Django 5.1.3 on 2024-12-14 19:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_system', '0007_lesson_edited_lesson_last_edited_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
