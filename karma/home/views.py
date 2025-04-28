from django.shortcuts import render, redirect
from .forms import SignUpForm, loginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home/index.html')

def blog(request):
    return render(request, 'home/pages/blog/blog.html')

def blog_details(request):
    return render(request, 'home/pages/blog/blog_details.html')

def shop_products(request):
    return render(request, 'home/pages/shop/products.html')

def shop_product_details(request):
    return render(request, 'home/pages/shop/product_details.html')

def shop_cart(request):
    return render(request, 'home/pages/shop/cart.html')

def shop_checkout(request):
    return render(request, 'home/pages/shop/checkout.html')

def shop_confirmation(request):
    return render(request, 'home/pages/shop/confirmation.html')

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Welcome Back')
                return redirect('vendor_dashboard')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
    else:
        form = loginForm()
    context={
        'form':form
    }
    return render(request, 'home/pages/auth/login.html', context)

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = SignUpForm()
    context={
        'form':form
    }
    return render(request, 'home/pages/auth/register.html', context)

def contact(request):
    return render(request, 'home/pages/contact.html')

def logout(request):
    return render(request, 'home/index.html')

def admin_login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Welcome Back')
                return redirect('vender_dashboard')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
    else:
        form = loginForm()
    context={
        'form':form
    }
    return render(request, 'home/pages/auth/admin_login.html', context)