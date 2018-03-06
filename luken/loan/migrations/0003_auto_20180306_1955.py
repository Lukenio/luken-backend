# Generated by Django 2.0.2 on 2018-03-06 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_auto_20180305_0645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanapplication',
            old_name='bitcoin_collateral',
            new_name='crypto_collateral',
        ),
        migrations.RenameField(
            model_name='loanapplication',
            old_name='bitcoin_price_usd',
            new_name='crypto_price_usd',
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='crypto_type',
            field=models.SmallIntegerField(choices=[(0, 'Bitcoin'), (1, 'Etherium')], default=1),
            preserve_default=False,
        ),
    ]
