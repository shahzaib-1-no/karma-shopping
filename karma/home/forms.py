from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (BillingDetails,)

class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User    
        fields = ('username', 'email', 'password1', 'password2')    
        widgets={
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control',}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    def clean_username(self):
        username= self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return self.cleaned_data
    
class loginForm(forms.Form):
    username= forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password= forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields=['first_name', 'last_name', 'email', 'phone', 'country', 'state', 'city',
                'zip_code', 'payment_mode', 'payment_gateway', 'address']
        widgets={
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'payment_mode': forms.RadioSelect(),
            'payment_gateway': forms.RadioSelect(),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }
    def clean_payment_gateway(self):
        cleaned_data = super().clean()  
        payment_mode = cleaned_data.get('payment_mode')
        payment_gateway = cleaned_data.get('payment_gateway')
        if payment_mode == 'card' and payment_gateway not in ['stripe', 'paypal']:
            raise forms.ValidationError("For Card Payment Gateway, only Stripe or Paypal is allowed.")

        return payment_gateway
    def clean_payment_mode(self):
        cleaned_data = super().clean()  
        payment_mode = self.cleaned_data.get('payment_mode')
        payment_gateway = self.cleaned_data.get('payment_gateway')
        if payment_mode == 'cash' and payment_gateway != 'cash':
            raise forms.ValidationError("For Cash Payment Gateway, only Cash is allowed.")
        return payment_mode
    
