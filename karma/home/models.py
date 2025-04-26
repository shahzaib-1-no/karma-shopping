from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Header(models.Model):
    image = models.ImageField("Header Image", upload_to="landing_page/header/", null=False, blank=False)
    title = models.CharField("Header Title", max_length=100, null=False, blank=False)
    created_at = models.DateTimeField("Header Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Header Updated Date", auto_now=True)

    def __str__(self):
        return self.title

class Banner(models.Model):
    image= models.ImageField("Banner Image",upload_to="landing_page/banner/", null=False, blank=False)
    title= models.CharField("Banner Title",max_length=100, null=False, blank=False)
    description= models.TextField("Banner Description",null=False, blank=False)
    created_at= models.DateTimeField("Banner Created Date",auto_now_add=True)
    updated_at= models.DateTimeField("Banner Updated Date",auto_now=True)

    def __str__(self):
        return self.title

class Services(models.Model):
    title= models.CharField("Service Title",max_length=100, null=False, blank=False)
    description= models.TextField("Service Description",null=False, blank=False)
    image= models.ImageField("Service Image",upload_to="landing_page/services/", null=False, blank=False)
    created_at= models.DateTimeField("Service Created Date",auto_now_add=True)
    updated_at= models.DateTimeField("Service Updated Date",auto_now=True)

    def __str__(self):
        return self.title

class ContentSection(models.Model):
    section_type= models.CharField("Content Section Type",max_length=100, null=False, blank=False)
    title= models.CharField("Content Section Title",max_length=100, null=False, blank=False)
    description= models.TextField("Content Section Description",null=False, blank=False)
    created_at= models.DateTimeField("Content Section Created Date",auto_now_add=True)
    updated_at= models.DateTimeField("Content Section Updated Date",auto_now=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    title= models.CharField("Category Title",max_length=100, null=False, blank=False)
    created_at= models.DateTimeField("Category Created Date",auto_now_add=True)
    updated_at= models.DateTimeField("Category Updated Date",auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    image= models.ImageField("Product Image",upload_to="landing_page/product/", null=False, blank=False)
    title= models.CharField("Product Title",max_length=100, null=False, blank=False)
    category= models.ForeignKey(Category, on_delete=models.CASCADE,related_name="products")
    quantity= models.IntegerField("Product Quantity",null=False, blank=False)
    price= models.IntegerField("Product Price",null=False, blank=False)
    description= models.TextField("Product Description",null=False, blank=False)
    created_at= models.DateTimeField("Product Created Date",auto_now_add=True)
    updated_at= models.DateTimeField("Product Updated Date",auto_now=True)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField("Cart Item Quantity", null=False, blank=False)
    price = models.DecimalField("Cart Item Price", max_digits=10, decimal_places=2, null=False, blank=False)
    created_at = models.DateTimeField("Cart Item Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Cart Item Updated Date", auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.quantity} x {self.price}"
    
class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="billing_details")
    first_name = models.CharField("First Name", max_length=100, null=False, blank=False)
    last_name = models.CharField("Last Name", max_length=100, null=False, blank=False)
    email = models.EmailField("Email", max_length=100, null=False, blank=False)
    phone = models.CharField("Phone", max_length=100, null=False, blank=False)
    country = models.CharField("Country", max_length=100, null=False, blank=False)
    state = models.CharField("State", max_length=100, null=False, blank=False)
    city = models.CharField("City", max_length=100, null=False, blank=False)
    address = models.CharField("Address", max_length=255, null=False, blank=False)
    zip_code = models.CharField("Zip Code", max_length=20, null=False, blank=False)
    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    billing_details = models.ForeignKey(BillingDetails, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    total_amount = models.DecimalField("Total Amount", max_digits=10, decimal_places=2)
    status = models.CharField("Order Status", max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    note = models.TextField("Order Note", blank=True, null=True)
    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_amount}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items_product")
    quantity = models.IntegerField("Order Item Quantity", default=1)
    price = models.DecimalField("Order Item Price", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.quantity} x {self.price}"
    
class PaymentDetails(models.Model):
    PAYMENT_MODE_CHOICES=(
        ('cash', 'Cash'),
        ('card', 'Card'),
    )
    PAYMENT_GATEWAY_CHOICES=(
        ('stripe', 'Stripe'),
        ('paypal', 'Paypal'),
        
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment_details")
    payment_mode = models.CharField("Payment Mode", max_length=20, choices=PAYMENT_MODE_CHOICES, default='cash')
    payment_gateway = models.CharField("Payment Gateway", max_length=20, choices=PAYMENT_GATEWAY_CHOICES, default='stripe')
    first_name = models.CharField("First Name", max_length=100, null=False, blank=False)
    last_name = models.CharField("Last Name", max_length=100, null=False, blank=False)
    email = models.EmailField("Email", max_length=100, null=False, blank=False)
    phone = models.CharField("Phone", max_length=100, null=False, blank=False)
    address = models.CharField("Address", max_length=255, null=False, blank=False)
    zip_code = models.CharField("Zip Code", max_length=20, null=False, blank=False)
    card_number = models.CharField("Card Number", max_length=20, null=False, blank=False)
    card_expiry_month = models.CharField("Card Expiry Month", max_length=2, null=False, blank=False)
    card_expiry_year = models.CharField("Card Expiry Year", max_length=4, null=False, blank=False)
    card_cvv = models.CharField("Card CVV", max_length=4, null=False, blank=False)
    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"