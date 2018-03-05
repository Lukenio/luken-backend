# Generated by Django 2.0.2 on 2018-02-28 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinaccount',
            name='type',
            field=models.IntegerField(choices=[(0, 'Bitcoin'), (1, 'Bitcoin Cache'), (2, 'Litecoin')]),
        ),
        migrations.AlterField(
            model_name='coinaccount',
            name='vault_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]