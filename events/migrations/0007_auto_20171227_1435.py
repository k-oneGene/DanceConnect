# Generated by Django 2.0 on 2017-12-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_category_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ManyToManyField(to='events.Category'),
        ),
    ]
