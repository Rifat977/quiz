# Generated by Django 5.0.2 on 2024-03-17 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_rename_is_sequenced_questionpattern_random_serve'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattempt',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]