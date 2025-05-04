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
    path('admin_login/', views.admin_login, name='admin_login'),
    path('auth/register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:category>/title', views.category_title, name='category_title'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/item/', views.remove_from_cart, name='remove_from_cart'),
    path('create_checkout_session/<int:billing_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('cancel/', views.shop_cancel, name='cancel'),
    path('success/', views.shop_confirmation, name='success'),
]