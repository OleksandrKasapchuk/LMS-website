# Generated by Django 5.1.3 on 2024-12-15 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_system', '0009_answer_mark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='upload_data',
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='answer_media')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='course_system.answer')),
            ],
        ),
    ]
