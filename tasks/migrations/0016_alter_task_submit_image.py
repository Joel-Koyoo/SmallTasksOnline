# Generated by Django 4.0.5 on 2022-07-04 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_task_submit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='Submit_Image',
            field=models.ImageField(blank=True, null=True, upload_to='files'),
        ),
    ]
