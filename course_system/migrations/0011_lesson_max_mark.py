# Generated by Django 5.1.3 on 2024-12-15 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_system', '0010_remove_answer_upload_data_uploadedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='max_mark',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]