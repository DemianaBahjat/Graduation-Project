from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib import messages
from predict.models import Stroke
import matplotlib
matplotlib.use('Agg')
from collections import defaultdict
import matplotlib.pyplot as plt
from cycler import cycler
import base64 
from io import BytesIO
from scipy.interpolate import interp1d
import numpy as np
import random
# Create your views here.
def home(request):
    return render(request, "accounts/home.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Login user")
            login(request, user)
            return redirect(reverse('accounts:home'))
        else:
            messages.success(
                request, ("There are was an error logging in , Try again"))
            return redirect(reverse('accounts:login'))
    else:
        return render(request, "accounts/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(
        request, ("You are logged out"))
    return render(request, "accounts/log out.html")


def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('accounts:home'))
    else:
        form = SignupForm()
    return render(request, 'accounts/register.html', {'form': form})

def reset(request):
    return render(request, "accounts/reset.html")


def profile(request):
    profile = Profile.objects.get(user=request.user)
    other_stroke_predictions = Stroke.objects.filter(patient=request.user, patient_code=1).order_by('-date').first()
    my_stroke_predictions = Stroke.objects.filter(patient=request.user, patient_code=0).order_by('-date').first()
    results = Stroke.objects.filter(patient=request.user).order_by('date')
    filtered_results = [result for result in results if result.result_proba is not None]

    # Create lists of dates and probabilities from filtered results
    dates = [result.date for result in filtered_results]

    # Find the unique dates when stroke prediction was performed
    unique_dates = sorted(set(dates))

    # Determine the indices of the dates to use as ticks and their corresponding labels
    tick_interval = 7
    tick_indices = [i for i in range(len(unique_dates)) if i % tick_interval == 0]
    tick_labels = [unique_dates[i].strftime('%Y-%m-%d') for i in tick_indices]

    # Create a dictionary to store the cumulative probabilities for each date
    cumulative_probabilities = defaultdict(float)
    for result in filtered_results:
        cumulative_probabilities[result.date] += result.result_proba

    # Create lists of cumulative probabilities and corresponding dates
    cumulative_probabilities_list = np.clip([cumulative_probabilities[date] for date in unique_dates], 0, 100)

    # Find the dates and probabilities for user predictions
    pred_dates = [result.date for result in results if result.result_proba is not None]
    pred_probabilities = [result.result_proba for result in results if result.result_proba is not None]

    # Find the indices of the prediction dates in the unique dates list
    pred_indices = [unique_dates.index(date) for date in pred_dates]

    # Create arrays of prediction dates and probabilities
    pred_x = np.array(pred_indices)
    pred_y = np.array(pred_probabilities)

    # Interpolate the data using a cubic spline
    xnew = np.linspace(0, len(unique_dates)-1, 300)
    if len(unique_dates) <= 2:
        ynew_unclipped = np.interp(xnew, range(len(unique_dates)), cumulative_probabilities_list)
        # Calculate Z-scores for all y-values
        z_scores = (ynew_unclipped - np.mean(ynew_unclipped)) / np.std(ynew_unclipped)
        z_score_threshold = 3
        ynew = np.where(np.abs(z_scores) > z_score_threshold, np.nan, ynew_unclipped)
        ynew = np.nan_to_num(ynew)

    else:
        # Use cubic spline interpolation
        f = interp1d(range(len(unique_dates)), cumulative_probabilities_list, kind='cubic')
        ynew = np.minimum(100, np.maximum(0, f(xnew)))
        # ynew = f(xnew)

    
    my_style = {
        'figure.figsize': (6, 2),
        'axes.prop_cycle': cycler('color', ['dodgerblue', '#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43']),
        'lines.linewidth': 3,
        'lines.markersize': 5,
        'grid.color': 'gray', 
        'grid.linestyle': '--',
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica Neue', 'Arial', 'sans-serif'],
        'text.color': 'black',
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'axes.labelsize': 14,
        'axes.labelweight': 'bold',
        'axes.titlesize': 16,
        'axes.titleweight': 'bold'
    }
    plt.style.use(my_style)
    plt.rcParams['axes.facecolor'] = '#DCDCDC'


    
    fig, ax = plt.subplots()
    # Fill the area under the curve
    ax.fill_between(xnew, ynew, 0, alpha=0.2)
    
    ax.plot(xnew, ynew, linewidth=3)


    for x, y in zip(pred_x, pred_y):
        indices = np.where(np.abs(xnew - x) < 0.01)[0]
        for i in indices:
            jittered_x = xnew[i] + random.uniform(-0.1, 0.1)
            ax.plot(jittered_x, y, marker='o', markersize=9, color='dodgerblue', markeredgecolor='grey', linewidth=2)
    
    ax.set_xticks(tick_indices)
    ax.set_xticklabels(tick_labels, fontsize='medium')
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability', fontsize=12, fontweight='bold')
    ax.set_title('Stroke Probability Over Time', fontsize=14, fontweight='bold')
    ax.grid(color='gray', linestyle='--', linewidth=0.5) 
    fig.tight_layout()


    # Save the figure to a bytes buffer
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'profile': profile,
        'unique_dates': len(unique_dates), 
        'image_data': image_data,
        'my_stroke' : my_stroke_predictions,
        'other_stroke': other_stroke_predictions,
    }
    return render(request, 'accounts/profile.html', context)


def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        userform = UserForm(request.POST, instance=request.user)
        profileform = ProfileForm(
            request.POST, request.FILES, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            return redirect(reverse('accounts:profile'))
    else:
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)
    context = {
        'userform': userform,
        'profileform': profileform,
    }
    return render(request, 'accounts/Edit profile.html', context)
