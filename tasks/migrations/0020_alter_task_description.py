# Generated by Django 4.0.5 on 2022-08-17 15:46

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0019_task_submit_description_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
