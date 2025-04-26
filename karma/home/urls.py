from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('blog/', views.blog, name='blog'),
    path('blog/details/', views.blog_details, name='blog_details'),
    path('shop/products/', views.shop_products, name='shop_products'),
    path('shop/product/details/', views.shop_product_details, name='shop_product_details'),
    path('shop/cart/', views.shop_cart, name='shop_cart'),
    path('shop/checkout/', views.shop_checkout, name='shop_checkout'),
    path('shop/confirmation/', views.shop_confirmation, name='shop_confirmation'),
    path('auth/login/', views.login, name='login'),
    path('auth/register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
]