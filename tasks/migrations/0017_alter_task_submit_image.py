# Generated by Django 4.0.5 on 2022-07-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_alter_task_submit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='Submit_Image',
            field=models.ImageField(blank=True, default='profile_pic.jpg', null=True, upload_to='files'),
        ),
    ]
