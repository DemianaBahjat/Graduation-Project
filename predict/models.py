from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
# Create your models here.

class Diet(models.Model):
    diet_code = models.IntegerField(primary_key=True)
    diet_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.diet_name
    
class Stroke(models.Model):
    work = [
        (0, 'Private'),
        (1, 'Self Employed'),
        (2, 'Government Job'),
    ]
    gen = [
        (0, 'Male'),
        (1, 'Female'),
    ]
    hyper = [
        (1, 'Have hypertension'),
        (0, 'Not have hypertension'),
    ]
    heart = [
        (1, 'Have heart diseases'),
        (0, 'Not have heart diseases')
    ]
    patient_code = [
        (1, "Other"),
        (0, "Me")
    ]
    stroke_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    age = models.BigIntegerField()
    avg_glucose_level = models.FloatField()
    gender = models.IntegerField(choices=gen)
    work_type = models.IntegerField(choices=work)
    hypertension = models.IntegerField(choices=hyper)
    heart_disease = models.IntegerField(choices=heart)
    height = models.FloatField()
    weight = models.FloatField()
    result = models.FloatField()
    result_proba = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True)
    recommendation = models.ForeignKey(
        Diet, on_delete=models.CASCADE, null=True, blank=True)
    patient_code = models.IntegerField(choices=patient_code, null=True)




class Stroke_Diet_Map(models.Model):
    case_id = models.IntegerField(primary_key=True)
    diet_code = models.ForeignKey(Diet, on_delete=models.CASCADE, null=True)
    age_from = models.IntegerField()
    age_to = models.IntegerField()
    avg_glucose_level_from = models.FloatField()
    avg_glucose_level_to = models.FloatField()
    bmi_from = models.FloatField()
    bmi_to = models.FloatField()


class Live_data(models.Model):
    input_data = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
