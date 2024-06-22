import pickle
import random
import pandas as pd
import numpy as np
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import PredictionForm
from .models import *
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

@login_required
def predict(request):
    live_data = Live_data.objects.filter(user=request.user).order_by('-date')
    if live_data:
        numbers = []
        for data in live_data[:12]:
            numbers.append(int(round(float(str(data.input_data)[-12:]))))
        # If there are less than 12 entries, pad with zeros
        numbers += [0] * (12 - len(numbers))
    else:
        numbers = [random.randint(70, 85) for _ in range(12)]

    # Smooth the data
    x_smooth = np.linspace(1, 12, 300)
    spline = make_interp_spline(range(1, 13), numbers)
    y_smooth = spline(x_smooth)

    # Create the chart
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    ax.plot(x_smooth, y_smooth, color='blue', linewidth=1.5)
    ax.set_title('Heart Rate', fontsize=8, fontweight='bold')
    ax.set_xlabel('Count', fontsize=6)
    ax.set_ylabel('Heart Pulses', fontsize=6)
    ax.tick_params(axis='both', which='major', labelsize=6)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Render the chart as an image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    chart_image = buf.getvalue()
    chart_image_b64 = base64.b64encode(chart_image).decode('utf-8')
    plt.close(fig)

    # Read and clean the data
    if request.method == "POST" and "form_name" in request.POST and request.POST["form_name"] == "form1":
        form = PredictionForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            hypertension = form.cleaned_data['hypertension']            
            work_type = form.cleaned_data['work_type']
            heart_disease = form.cleaned_data['heart_disease']
            avg_glucose_level = form.cleaned_data['avg_glucose_level']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            patient_code = form.cleaned_data['patient_code']
            BMI = float(weight) / float(((height / 100) * (height / 100)))


            # Load the trained model from file
            with open('X:\\Stroke\\Stroke-Prediction-Test\\predict\\sklearn_stroke_model.pkl', 'rb') as f:
                model = pickle.load(f)

                # Make prediction
            result = model.predict(
                [[gender, age, hypertension, heart_disease, work_type, avg_glucose_level, BMI]])
            
            result_proba = model.predict_proba(
                pd.DataFrame([[gender, age, hypertension, heart_disease, work_type, avg_glucose_level, BMI]], 
                            columns=['gender', 'age', 'hypertension', 'heart_disease', 'work_type', 'avg_glucose_level', 'bmi']))
            
            result_yes = result_proba[:, 1]
            
            if result_yes > 0.5:
               final_result = np.round(result_yes * 100 , 2) 
            else:
                final_result = 0

                # Query to the recommendation system
            diet_map = Stroke_Diet_Map.objects.filter(
                Q(age_from__lte=age) & Q(age_to__gte=age),
                Q(avg_glucose_level_from__lte=avg_glucose_level) &
                Q(avg_glucose_level_to__gte=avg_glucose_level),
                Q(bmi_from__lte=BMI) & Q(bmi_to__gte=BMI)).first()

                # Retrieved diet code
            diet = diet_map.diet_code

                # Create a new Stroke object and save it to the database
            stroke = Stroke.objects.create(
                age=age,
                gender=gender,
                hypertension=hypertension,
                work_type=work_type,
                heart_disease=heart_disease,
                avg_glucose_level=avg_glucose_level,
                height=height,
                weight=weight,
                recommendation=diet,
                result=result,
                result_proba = final_result, 
                patient_code = patient_code,
                patient=request.user,
            )
            stroke.save()

            # Render the result page with the prediction result
            return render(request, 'predict/result.html', {'result': final_result, 'diet': diet})
        
    elif request.method == "POST" and "form_name" in request.POST and request.POST["form_name"] == "form2":
        avg = sum(numbers) / len(numbers)
        print(avg)
        with open('X:\\Stroke\\Stroke-Prediction-Test\\predict\\heart_pulses_hypertension_model.pkl', 'rb') as h:
                    hyer_model = pickle.load(h)           
        # Put the data into a data frame 
        random_nums = pd.DataFrame([[avg]], columns=[['heart_pulses']])
        # Convert column names to strings
        random_nums.columns = ['heart_pulses']
        # The result of prediction
        heart_hyper_result = hyer_model.predict(random_nums).tolist()
        print("Heart Pulses Result is ", heart_hyper_result)
        return JsonResponse({'heart_hyper_result': heart_hyper_result})


    else:
        form = PredictionForm()

    return render(request, 'predict/prediction.html', {'form': form, 'numbers': numbers,'chart_image': chart_image_b64,})


def result(request):
    return render(request, 'predict/result.html', {})

def diets(request):
    return render(request, 'predict/dite plan.html')


def compass(request):
    live_data = Live_data.objects.filter(user=request.user).order_by('-date')
    if live_data:
        numbers = []
        for data in live_data[:12]:
            numbers.append(int(round(float(str(data.input_data)[-12:]))))
        # If there are less than 12 entries, pad with zeros
        numbers += [0] * (12 - len(numbers))
    else:
        numbers = [random.randint(70, 85) for _ in range(12)]
    return render(request, 'predict/compass.html' , {'numbers': numbers})