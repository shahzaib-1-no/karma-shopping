from django.shortcuts import render

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
    return render(request, 'home/pages/auth/login.html')

def register(request):
    return render(request, 'home/pages/auth/register.html')

def contact(request):
    return render(request, 'home/pages/contact.html')