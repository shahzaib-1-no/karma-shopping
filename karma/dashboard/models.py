from django.db import models
from django.contrib.auth.models import User
from home.models import PaymentRecord,Category
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


# Create your models here.
class RefundRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(PaymentRecord, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Refund Request - {self.order.pk} by {self.user.username}"
    
class Blog(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog')
    image= models.ImageField(upload_to='blog_images/')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    tags = TaggableManager()
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Blog - {self.title}"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

