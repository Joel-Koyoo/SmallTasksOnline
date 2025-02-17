# Generated by Django 4.0.5 on 2022-07-02 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=200, null=True)),
                ('LastName', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=60, null=True)),
                ('picture', models.ImageField(blank=True, default='profile_pic.jpg', null=True, upload_to='pictures/')),
                ('is_taskhandler', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deadline_Day', models.DateTimeField(blank=True, null=True)),
                ('deadline_Time', models.DateTimeField(blank=True, null=True)),
                ('Proposed_price', models.FloatField(null=True)),
                ('category', models.CharField(choices=[('Computer Science', 'Computer Science'), ('Business and Finance', 'Business and finance'), ('Academic Writing', 'Academic Writing'), ('Assignment Handling', 'Assignment Handling'), ('Essay Writing', 'Essay Writing')], max_length=200, null=True)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Claimed', 'Claimed'), ('Completed', 'Completed'), ('submitted', 'submitted')], default='Available', max_length=200, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='files')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.client')),
                ('taskhandler', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='tasks.client')),
            ],
        ),
    ]
