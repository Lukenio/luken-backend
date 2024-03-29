# Generated by Django 2.0.2 on 2018-03-31 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0005_auto_20180325_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=20)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pub_address', models.CharField(max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coins.CoinAccount')),
            ],
        ),
    ]
