# Generated by Django 2.0.2 on 2018-05-01 13:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_kyc'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 5, 1, 13, 6, 6, 636291, tzinfo=utc)),
            preserve_default=False,
        ),
    ]