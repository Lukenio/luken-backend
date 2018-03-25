# Generated by Django 2.0.2 on 2018-03-25 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_auto_20180306_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='apr',
            field=models.DecimalField(decimal_places=2, default=0.2, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='ltv',
            field=models.DecimalField(decimal_places=2, default=0.35, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='total_loaned_amount',
            field=models.DecimalField(decimal_places=2, default=20000.01, max_digits=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loanapplication',
            name='state',
            field=models.SmallIntegerField(choices=[(0, 'Submitted'), (1, 'In Review'), (2, 'Approved'), (3, 'Declined'), (4, 'Funded'), (5, 'Loan released')], default=0),
        ),
    ]
