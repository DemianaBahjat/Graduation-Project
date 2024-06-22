from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, EmailValidator
from .models import *


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'example@email.com'}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password confirm'}))

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        regex = '^[a-zA-Z]+$'
        validator = RegexValidator(
            regex=regex,
            message='First name should contain only letters',
            code='invalid_first_name'
        )
        validator(first_name)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        regex = '^[a-zA-Z]+$'
        validator = RegexValidator(
            regex=regex,
            message='Last name should contain only letters',
            code='invalid_first_name'
        )
        validator(last_name)
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        validator = EmailValidator(
            message='Invalid Email Address',
            code='invalid_email'
        )
        validator(email)
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                    'last_name', 'password1', 'password2')
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "User Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "example@email.net"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',  'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age', 'phone', 'address' , 'image')
