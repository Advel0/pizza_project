# Generated by Django 3.0.7 on 2020-06-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]