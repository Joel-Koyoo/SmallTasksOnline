# Generated by Django 4.0.6 on 2022-07-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='Submit_Description_report',
            field=models.TextField(blank=True, null=True),
        ),
    ]
