# Generated by Django 2.0.2 on 2018-02-08 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20180130_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionpaypal',
            name='status',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
