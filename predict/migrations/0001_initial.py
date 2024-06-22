# Generated by Django 3.2.18 on 2023-03-14 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='stroke',
            fields=[
                ('stroke_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('age', models.BigIntegerField()),
                ('avg_glucose_level', models.FloatField()),
                ('ever_married', models.BinaryField()),
                ('hypertension', models.BinaryField()),
                ('heart_disease', models.BinaryField()),
                ('result', models.BigIntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('recommend_one', models.CharField(max_length=255)),
                ('recommend_two', models.CharField(max_length=255)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]