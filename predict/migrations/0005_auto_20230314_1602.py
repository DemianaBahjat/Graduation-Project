# Generated by Django 3.2.18 on 2023-03-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0004_diet_stroke_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diet',
            name='stroke_id',
            field=models.ManyToManyField(to='predict.Stroke'),
        ),
        migrations.CreateModel(
            name='Stroke_Diet_Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_from', models.IntegerField()),
                ('age_to', models.IntegerField()),
                ('avg_glucose_level_from', models.FloatField()),
                ('avg_glucose_level_to', models.FloatField()),
                ('hypertension', models.BinaryField()),
                ('diet_one', models.ManyToManyField(to='predict.Diet')),
            ],
        ),
    ]
