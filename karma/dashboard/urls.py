from django.urls import path
from . import views

urlpatterns = [
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.logout, name='logout'),
    
    ### Category Pages ###
    path('admin/category/', views.category, name='category'),
    path('admin/category/<int:id>/delete/', views.category_delete, name='category_delete'),
    ### Category Pages End ###
    
    ### Product Pages ###
    path('admin/product/', views.product, name='product'),
    path('admin/product/create/', views.product_create, name='product_create'),
    path('admin/product/<int:id>/delete/', views.product_delete, name='product_delete'),
    path('admin/product/<int:id>/update/', views.product_update, name='product_update'),
    ### Product Pages End ###
    
    ### Admin Order Pages ###
    path('admin/orders/', views.orders, name='orders'),
    path('admin/order/<int:id>/details/', views.order_details, name='order_details'),
    path('admin/order/refund/', views.order_refund, name='order_refund'),
    path('admin/order/<int:id>/refund/reject/', views.order_refund_reject, name='order_refund_reject'),
    path('admin/order/<int:id>/refund/approve/', views.order_refund_approve, name='order_refund_approve'),
    ### Admin Order Pages End ###
    
    ### Client Order Pages ###
    path('client/orders/', views.client_orders, name='client_orders'),
    path('client/order/<int:id>/details/', views.client_order_details, name='client_order_details'),
    path('client/order/<int:id>/refund/', views.client_order_refund_request, name='client_order_refund_request'),
]