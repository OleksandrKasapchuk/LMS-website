# Generated by Django 5.1.4 on 2025-01-10 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
    ]
