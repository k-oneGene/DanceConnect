# Generated by Django 2.0.1 on 2018-01-12 12:44

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20180112_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=events.models.event_name_path),
        ),
    ]
