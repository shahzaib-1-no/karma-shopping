from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, loginForm, BillingDetailsForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from .models import (Product,Category,BillingDetails, CartItem, PaymentRecord)
from django.db.models import Count
from django.contrib.sessions.models import Session
from pprint import pprint
import stripe
from django.utils.timezone import make_aware
from datetime import datetime
from dashboard.models import (Blog,)

stripe.api_key = "ENTER YOUR STRIPE API KEY"

# Create your views here.
def home(request):
    return render(request, 'home/index.html')

def blog(request):
    blogs = Blog.objects.all().order_by('-id')
    context={
        'blogs':blogs
        }
    return render(request, 'home/pages/blog/blog.html',context)

def blog_details(request , id):
    blog = get_object_or_404(Blog, pk=id)
    context={
        'blog':blog
        }
    return render(request, 'home/pages/blog/blog_details.html',context)

def shop_products(request):
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.annotate(product_count=Count(Product)).filter(product_count__gt=0).order_by('-id')
    context={
        'products':products,
        'categories':categories
        }
    return render(request, 'home/pages/shop/products.html', context)

def category_title(request, category):
    products = Product.objects.filter(category__title=category).order_by('-id')
    categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0).order_by('-id')
    context={
        'products':products,
        'categories':categories
        }
    return render(request, 'home/pages/shop/products.html', context)

def add_to_cart(request, id):
    if request.user.is_authenticated:
        pass
    else:
        products= Product.objects.get(pk=id)
        cart= request.session.get('cart',[])
        if cart is None:
            cart = []  # Initialize the cart as an empty list if it doesn't exist in session
            
        cart_item = next((item for item in cart if item['product_id'] == id), None)
        
        if cart_item is None:
            # Add the product_id to the cart (store it as a dictionary with 'product_id' as the key)
            cart.append(
                {'product_id': id, 'quantity': 1, 'product_count': 1, 'price': products.price, 'total': products.price*1}
                )
            
            # Save the updated cart back to session
            request.session['cart'] = cart
            
            # Succes message to display to the user
            messages.success(request, 'Product Added to Cart')
        else:
            cart_item['quantity'] += 1
            cart_item['total'] = cart_item['price'] * cart_item['quantity']
            
            request.session['cart'] = cart
            
            messages.success(request, 'Product Added to Cart')
    return redirect('shop_products')

def remove_from_cart(request, id):
    if request.user.is_authenticated:
        pass
    else:
        cart= request.session.get('cart')
        if cart is None:
            cart = []  # Initialize the cart as an empty list if it doesn't exist in session
        
        # Remove the product_id from the cart (store it as a dictionary with 'product_id' as the key)
        cart = [item for item in cart if item['product_id'] != id]
        
        # Save the updated cart back to session
        request.session['cart'] = cart
        
        # Succes message to display to the user
        messages.success(request, 'Product Removed from Cart')
    return redirect('shop_cart')

def shop_product_details(request):
    return render(request, 'home/pages/shop/product_details.html')

def shop_cart(request):
    total=0
    data= request.session.get('cart',[])
    ids= [items['product_id'] for items in data]
    products= Product.objects.in_bulk(ids)
    for product in products.values():
        quantity = next((item['quantity'] for item in data if item['product_id'] == product.id), 0)
        product.quantity = quantity 
        total += product.price * product.quantity
    context={'products':products, 'total':total}
    return render(request, 'home/pages/shop/cart.html', context )

def shop_checkout(request):
    check_data= request.session.get('cart',[])
    if not check_data:
        messages.error(request, 'Cart is Empty')
        return redirect('shop_cart')
    ### Step 1: Check's User Is Authenticated Or Not ###
    if request.user.is_authenticated:
        pass
    ### Step 1: End ###
    else:
        ### Step 2: Making a Session For Cart Items ###
        subtotal=0
        shipping_fees= 50
        cart_item= request.session.get('cart')
        ids= [items['product_id'] for items in cart_item]
        products= Product.objects.in_bulk(ids)
        for item in cart_item:
            product = products.get(item['product_id'])
            if product:
                item['title'] = product.title
        subtotal = sum(item['total'] for item in cart_item)
        final_total= subtotal + shipping_fees
        data={'subtotal':subtotal, 'shipping_fees':shipping_fees, 'final_total':final_total}
        ### Step 2: End ###
        
        if request.method == 'POST':
            form = BillingDetailsForm(request.POST)
            
            if form.is_valid():
                print(f"This is Form Data ::\n {form.cleaned_data}")
                create_account= request.POST.get('account_create')
                ### Step 3:  Create Account ###
                if create_account == 'on':
                    first_name= form.cleaned_data.get('first_name')
                    last_name= form.cleaned_data.get('last_name')
                    email= form.cleaned_data.get('email')
                    user_name= request.POST.get('user_name')
                    password1= request.POST.get('password1')
                    password2= request.POST.get('password2')
                    if password1 != password2:
                        messages.error(request, 'Passwords do not match')
                        return redirect('shop_checkout')
                    if user_name:
                        user = User.objects.filter(username=user_name).exists()
                        if user:
                            messages.error(request, 'Username already exists')
                            return redirect('shop_checkout')
                    try:
                       User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=user_name, 
                        password=password1,
                        email=email
                        )
                    except Exception as e:
                        messages.error(request, f"Wile creating user, error {e}")
                        return redirect('shop_checkout')
                    
                    try:
                        user = authenticate(request, username=user_name, password=password1)
                        auth_login(request, user)
                    except Exception as e:
                        messages.error(request, f"Wile authenticating user, error {e}")
                        return redirect('shop_checkout')
                    
                ### Step 3:  End ###
                billing=form.save(commit=False)
                if user:
                    billing.user = user
                billing.save()
                billing_id= billing.id
                cart_item= request.session.get('cart',[])
                for item in cart_item:
                    CartItem.objects.create(
                        billing_details=billing,
                        product_id=Product.objects.get(pk=item['product_id']),
                        quantity=item['quantity'],
                        price=item['price'],
                        total=item['total']
                    )
                
                payment_gateway= form.cleaned_data.get('payment_gateway')
                if payment_gateway == 'stripe':
                    return redirect('create_checkout_session', billing_id=billing_id)
                if payment_gateway == 'paypal':
                    messages.error(request, 'Paypal Not Implemented Yet')
                    return redirect('shop_checkout')
                if payment_gateway == 'cash':
                    messages.error(request, 'Cash Not Implemented Yet')
                    return redirect('shop_checkout')
        else:
            form = BillingDetailsForm()
        context={
            'form':form,
            'cart_item':cart_item,
            'data':data
        }
    return render(request, 'home/pages/shop/checkout.html', context)

def create_checkout_session(request, billing_id):
    print("Start Hogaya")
    DOMAIN='http://localhost:8000'
    cart_items = CartItem.objects.filter(billing_details__id=billing_id)
    line_items=[]
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(item.product_id.price * 100),  # cents
                'product_data': {
                    'name': item.product_id.title,
                },
            },
            'quantity': item.quantity,
        })
    success_url = f"{DOMAIN}/success/?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{DOMAIN}/cancel/?session_id={{CHECKOUT_SESSION_ID}}"

    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        customer_email=item.billing_details.email,  
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={'billing_id': str(billing_id)}
    )
    return redirect(checkout_session.url, code=303)

def shop_confirmation(request):
    #### This Part Is For Getting Data From Session ID  And Payment Intent ####
    request.session['cart'] = []
    session_id = request.GET.get('session_id')
    if not session_id:
        print("Session ID missing!")
        # return render(request, 'error.html', {'message': 'Session ID missing!'})

    session = stripe.checkout.Session.retrieve(session_id)
    print("This Is Session")
    print(session)
    if session.payment_intent:
        payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
        print("This Is Payment Intent")
        print(payment_intent)
        
    #### This Part Is Complelted ####
    
    #### This Part Is For Storing Payment Records in Database AND Updating Billing Details Property name STATUS as 'paid' ####
    
     # Get billing_id from metadata
    billing_id = session.metadata.get('billing_id')
    billing = get_object_or_404(BillingDetails, id=billing_id)
    billing.status = 'paid'
    billing.save()

    # Optional: Get charge details
    charge_id = payment_intent.latest_charge if hasattr(payment_intent, 'latest_charge') else None

    # Payment datetime
    paid_at = make_aware(datetime.fromtimestamp(payment_intent.created))
    
    payment_record, created = PaymentRecord.objects.get_or_create(
        session_id=session.id,
        defaults={
            'billing': billing,
            'payment_intent': payment_intent.id,
            'charge_id': charge_id,
            'amount_total': session.amount_total,
            'amount_received': payment_intent.amount_received,
            'currency': session.currency,
            'payment_status': session.payment_status,
            'stripe_status': payment_intent.status,
            'customer_name': session.customer_details.get('name') if session.customer_details else None,
            'customer_email': session.customer_email,
            'payment_method': payment_intent.payment_method,
            'paid_at': paid_at,
        }
    )

    
    #### This Part Is Complelted ####
    
    context={
        'payment_intent': payment_intent,
        'session': session,
        'billing': billing,
        'data': payment_record
    }
    return render(request, 'home/pages/shop/confirmation.html', context)

def shop_cancel(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    billing_id = session.metadata.get('billing_id')
    billing = get_object_or_404(BillingDetails, id=billing_id)
    billing.status = 'cancelled'
    billing.save()
    return render(request, 'home/pages/shop/cancel.html')

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