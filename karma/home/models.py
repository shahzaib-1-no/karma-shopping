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

class BillingDetails(models.Model):
    PAYMENT_MODE_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
    )

    PAYMENT_GATEWAY_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'Paypal'),
        ('cash', 'Cash'),
    )
    
    STATUS_CHOICES = (
    ('pending', 'Pending'),  # Default status
    ('paid', 'Paid'),
    ('failed', 'Failed'),
    ('cancelled', 'Cancelled'),
    )

    payment_mode = models.CharField("Payment Mode", max_length=20, choices=PAYMENT_MODE_CHOICES, default='cash')
    payment_gateway = models.CharField("Payment Gateway", max_length=20, choices=PAYMENT_GATEWAY_CHOICES, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="billing_details")
    first_name = models.CharField("First Name", max_length=100)
    last_name = models.CharField("Last Name", max_length=100)
    email = models.EmailField("Email", max_length=100)
    phone = models.CharField("Phone", max_length=20)
    country = models.CharField("Country", max_length=100)
    state = models.CharField("State", max_length=100)
    city = models.CharField("City", max_length=100)
    address = models.CharField("Address", max_length=255)
    zip_code = models.CharField("Zip Code", max_length=20)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CartItem(models.Model):
    billing_details = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, related_name="cart_item")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField("Cart Item Quantity", null=False, blank=False)
    price = models.DecimalField("Cart Item Price", max_digits=10, decimal_places=2, null=False, blank=False)
    total= models.DecimalField("Cart Item Total", max_digits=10, decimal_places=2, null=False, blank=False)
    created_at = models.DateTimeField("Cart Item Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Cart Item Updated Date", auto_now=True)
    
class PaymentRecord(models.Model):
    billing = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, related_name='payments')
    order_number = models.CharField(max_length=255, null=True, blank=True)
    # Stripe session/payment identifiers
    session_id = models.CharField(max_length=255,unique=True)
    payment_intent = models.CharField(max_length=255,unique=True)
    charge_id = models.CharField(max_length=255, null=True, blank=True)
    # Amounts & currency
    amount_total = models.IntegerField()  # in cents
    amount_received = models.IntegerField()  # in cents
    currency = models.CharField(max_length=10)
    # Payment status
    payment_status = models.CharField(max_length=50)  # Stripe session.payment_status (e.g., "paid")
    stripe_status = models.CharField(max_length=50)  # PaymentIntent.status (e.g., "succeeded", "requires_payment_method")
    # Customer info
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    # Payment method used
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    # Time fields
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.order_number:
            self.order_number = f"ORD-{self.pk:06d}"
            super().save(update_fields=['order_number'])