# Generated by Django 2.0.2 on 2018-03-13 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20180313_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='vender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='venders.Vender'),
        ),
    ]
