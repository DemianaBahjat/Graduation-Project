# Generated by Django 3.2.18 on 2023-03-21 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0007_auto_20230321_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diet',
            name='stroke_id',
            field=models.ManyToManyField(to='predict.Stroke'),
        ),
    ]