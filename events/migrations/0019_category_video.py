# Generated by Django 2.0.2 on 2018-03-13 15:14

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_event_vender'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='video', validators=[events.models.validate_file_extension]),
        ),
    ]
