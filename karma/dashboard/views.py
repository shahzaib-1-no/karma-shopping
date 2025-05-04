from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from home.models import ( Category, Product)
from .forms import ( CategoryForm, ProductForm, BlogForm)
from .services.order_services import (OrderServices,ClientOrderServices)
import pprint 
from .models import (Blog,)
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

#### ADMIN CATEGORY VIEWS START ####
    
@login_required
@user_passes_test(is_admin)
def category(request): # Create Category And Display All Categories
    categories = Category.objects.all().order_by('-id') # Get All Categories
    if request.method == 'POST': # If POST Request
        form = CategoryForm(request.POST) # Get Form Data
        if form.is_valid(): # If Form Is Valid
            form.save() # Save Form Data
            messages.success(request, 'Category created successfully') # Success Message
            return redirect('category') # Redirect To Category Page
    else:
        form = CategoryForm() # Get Empty Form
        
    context={
        'categories':categories,
        'form':form
    }
    return render(request, 'dashboard/admin_pages/category/category.html', context)

    
@login_required
@user_passes_test(is_admin)
def category_delete(request, id): # Delete Category
    category = Category.objects.get(pk=id)
    category.delete()
    messages.success(request, 'Category Deleted Successfully')
    return redirect('category')

@login_required
@user_passes_test(is_admin)
def product(request): # Display All Products
    products = Product.objects.all().order_by('-id')
    return render(request, 'dashboard/admin_pages/product/product.html', {'products':products})

@login_required
@user_passes_test(is_admin)
def product_create(request): # Create Product
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully')
            return redirect('product')
    else:
        form = ProductForm()
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/product/product_create.html', context)

@login_required
@user_passes_test(is_admin)
def product_delete(request, id): # Delete Product
    product = Product.objects.get(pk=id)
    product.delete()
    messages.success(request, 'Product Deleted Successfully')
    return redirect('product')

@login_required
@user_passes_test(is_admin)
def product_update(request, id): # Update Product
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('product')
    else:
        form = ProductForm(instance=product)
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/product/prduct_update.html', context)

#### ADMIN CATEGORY VIEWS END ####

#### ADMIN ORDER VIEWS START ####

@login_required
@user_passes_test(is_admin)
def orders(request): # Display All Orders With Billing Details
    orderservices= OrderServices()
    orders = orderservices.all_payments_with_billing()
    context={
        'orders':orders
    }
    return render(request, 'dashboard/admin_pages/orders/orders.html',context)

@login_required
@user_passes_test(is_admin)
def order_details(request, id): # Displaying Payment Details, Billing Details, Cart Items.
    orderservices= OrderServices()
    orders = orderservices.get_order_details(id)
    context={
        'orders':orders
    }
    return render(request, 'dashboard/admin_pages/orders/order_details.html',context)

@login_required
@user_passes_test(is_admin)
def order_refund(request): # Displaying Payment Details, Billing Details, Cart Items.
    orderservices= OrderServices()
    orders = orderservices.all_orders_refund()
    context={
        'orders':orders
    }
    return render(request, 'dashboard/admin_pages/orders/refund_orders.html',context)

@login_required
@user_passes_test(is_admin)
def order_refund_reject(request, id): # Reject Refund Request of Current Order
    orderservices= OrderServices()
    orders = orderservices.reject_refund_request(id)
    if orders is True:
        messages.success(request, 'Refund Request Rejected Successfully')
    else:
        messages.error(request, 'Refund Request Rejected Failed')
    return redirect('order_refund')

@login_required
@user_passes_test(is_admin)
def order_refund_approve(request, id): # Approve Refund Request of Current Order
    orderservices= OrderServices()
    orders = orderservices.approve_refund_request(id)
    if orders is True:
        messages.success(request, 'Refund Request Approved Successfully')
    else:
        messages.error(request, 'Refund Request Approved Failed')
    return redirect('order_refund')

#### ADMIN ORDER VIEWS END ####

#### CLIENT ORDER VIEWS START ####

@login_required
def client_orders(request): # Display All Orders With Billing Details For Client
    orderservices= ClientOrderServices()
    orders = orderservices.all_payments_with_billing(request.user)
    context={
        'orders':orders
    }
    return render(request, 'dashboard/client/orders.html',context)

@login_required
def client_order_details(request, id): # Displaying Payment Details, Billing Details, Cart Items.
    orderservices= ClientOrderServices()
    orders = orderservices.get_order_details(id)
    context={
        'orders':orders
    }
    return render(request, 'dashboard/client/order_details.html',context)

@login_required
def client_order_refund_request(request, id): # Requesting For Refund.
    request_refund = ClientOrderServices()
    result =request_refund.request_refund(id, request.user)
    if result is True:
        messages.success(request, 'Refund Requested Successfully Submitted, Waitting For Approval')
    else:
        messages.error(request, f"{result}")
    return redirect('client_orders')

#### CLIENT ORDER VIEWS END ####

#### ADMIN BLOG VIEWS START ####

@login_required
@user_passes_test(is_admin)
def blog(request): # Display All Blogs
    blogs = Blog.objects.all().order_by('-id')
    return render(request, 'dashboard/admin_pages/blog/blog.html', {'blogs':blogs})

@login_required
@user_passes_test(is_admin)
def blog_create(request): # Create Blog
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog created successfully')
            return redirect('admin_blog')
    else:
        form = BlogForm()
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/blog/blog_create.html', context)

@login_required
@user_passes_test(is_admin)
def blog_update(request, id): # Update Blog
    blog = Blog.objects.get(pk=id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully')
            return redirect('admin_blog')
    else:
        form = BlogForm(instance=blog)
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/blog/blog_update.html', context)

@login_required
@user_passes_test(is_admin)
def blog_delete(request, id): # Delete Blog
    blog = Blog.objects.get(pk=id)
    blog.delete()
    messages.success(request, 'Blog Deleted Successfully')
    return redirect('admin_blog')

#### ADMIN BLOG VIEWS END ####