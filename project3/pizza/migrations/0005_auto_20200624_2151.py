# Generated by Django 3.0.7 on 2020-06-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0004_order_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='money_amount',
            field=models.IntegerField(default=0),
        ),
    ]
