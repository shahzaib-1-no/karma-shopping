from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
# Create your views here.

#### AUTHENTICATION VIEWS START ####

def is_admin(user):
    return user.is_superuser

@login_required
def vendor_dashboard(request):
    is_superuser = request.user.is_superuser
    if is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')
    
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

@login_required
def user_dashboard(request):
    return render(request, 'dashboard/user_dashboard.html')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

#### AUTHENTICATION VIEWS END ####