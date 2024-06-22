# Generated by Django 3.2.18 on 2023-03-21 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0011_auto_20230321_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diet',
            name='stroke_id',
            field=models.ManyToManyField(to='predict.Stroke'),
        ),
        migrations.AlterField(
            model_name='stroke',
            name='avg_glucose_level',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='stroke',
            name='height',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='stroke',
            name='result',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='stroke',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]