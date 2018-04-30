# Generated by Django 2.0.2 on 2018-04-30 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpub', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='walletaddress',
            old_name='path',
            new_name='derivation_path',
        ),
        migrations.AddField(
            model_name='walletaddress',
            name='child',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='walletaddress',
            name='xpub',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]