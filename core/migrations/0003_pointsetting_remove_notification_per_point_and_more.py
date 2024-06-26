# Generated by Django 5.0.2 on 2024-03-06 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_notification_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_point', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='notification',
            name='per_point',
        ),
        migrations.AddField(
            model_name='notification',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
