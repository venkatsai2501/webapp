# Generated by Django 2.1.5 on 2024-11-20 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20241120_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='github_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='project',
            name='team_members',
        ),
        migrations.AddField(
            model_name='project',
            name='team_members',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]