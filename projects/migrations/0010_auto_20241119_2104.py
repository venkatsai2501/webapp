# Generated by Django 2.1.5 on 2024-11-19 15:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0009_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='faculty_members',
        ),
        migrations.AddField(
            model_name='project',
            name='faculty_members',
            field=models.ManyToManyField(blank=True, related_name='assigned_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]