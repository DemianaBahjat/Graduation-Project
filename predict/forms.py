from django import forms
from .models import Stroke
from django.core.exceptions import ValidationError

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Stroke
        fields = ['age', 'gender', 'hypertension', 'work_type',
                  'heart_disease', 'avg_glucose_level', 'height', 'weight', "patient_code"]
        
        widgets = {
            'age': forms.TextInput(attrs={'placeholder': 'Your Age'}),
            'gender': forms.Select(choices=[('', 'Select Gender'), (0, 'Male'), (1, 'Female')], attrs={'class': 'form-control'}),
            'hypertension': forms.Select(attrs={'id': 'hypertension-select'}),
            'height': forms.TextInput(attrs={'placeholder': 'Your Height'}),
            'weight': forms.TextInput(attrs={'placeholder': 'Your Weight (in kg)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        gender = cleaned_data.get('gender')
        hypertension = cleaned_data.get('hypertension')
        work_type = cleaned_data.get('work_type')
        heart_disease = cleaned_data.get('heart_disease')
        avg_glucose_level = cleaned_data.get('avg_glucose_level')
        height = cleaned_data.get('height')
        weight = cleaned_data.get('weight')
        patient_code = cleaned_data.get('patient_code')


        if height is None:
            raise forms.ValidationError(
                "Empty height")

        if weight is None:
            raise forms.ValidationError(
                "Empty weight.")

        if age < 0 or age > 120:
            raise forms.ValidationError("Please enter a valid age.")

        if hypertension not in [0, 1]:
            raise forms.ValidationError(
                "Please enter a valid hypertension value.")

        if heart_disease not in [0, 1]:
            raise forms.ValidationError(
                "Please enter a valid heart disease value.")

        if work_type not in [0, 1, 2]:
            raise forms.ValidationError("Please enter a valid work type.")

        BMI = float(weight) / float(((height / 100) * (height / 100)))
        if BMI < 15 or BMI > 70:
            raise forms.ValidationError(
                "Please enter a valid height and weight.")

        return cleaned_data