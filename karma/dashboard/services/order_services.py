from home.models import ( Product, CartItem, BillingDetails, PaymentRecord)
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Prefetch
from dashboard.models import RefundRequest
import stripe
from django.db import transaction
stripe.api_key = "ENTER YOUR STRIPE API KEY"


class OrderServices:
    
    def all_payments_with_billing(self):  
        return PaymentRecord.objects.select_related('billing').order_by('-id')
    
    def get_order_details(self, id):
        return PaymentRecord.objects.select_related('billing')\
            .prefetch_related('billing__cart_item__product_id')\
            .get(pk=id)
            
    def all_orders_refund(self):
        return RefundRequest.objects.select_related('order','order__billing').filter(status='pending').order_by('-id')
    
    def reject_refund_request(self, id):
        refund_data= RefundRequest.objects.get(pk=id)
        refund_data.status = 'rejected'
        refund_data.save()
        return True
    
    def approve_refund_request(self, id):
        refund_data= RefundRequest.objects.select_related('order').get(pk=id)
        charge_id=refund_data.order.charge_id
        if charge_id is None:
            return 'Charge Id Not Found'
        try:
            with transaction.atomic():
                stripe.Refund.create(
                    charge=charge_id
                )
                refund_data.status = 'approved'
                refund_data.save()
                return True
        except Exception as e:
            return str(e)
            
            
class ClientOrderServices:
    
    def all_payments_with_billing(self,User):  
        return PaymentRecord.objects.select_related('billing').filter(billing__user=User).order_by('-id')
        
    def get_order_details(self, id):
        return PaymentRecord.objects.select_related('billing')\
            .prefetch_related('billing__cart_item__product_id')\
            .get(pk=id)
            
    def request_refund(self, id, user):
        order= PaymentRecord.objects.get(pk=id)
        if RefundRequest.objects.filter(order = order , user = user).filter(status='pending').exists():
            return 'Refund Already Requested'
        if RefundRequest.objects.filter(order = order , user = user).filter(status='rejected').exists():
            return 'Your Refund Request is Rejected by Admin, which you do it before'
        
        try:
            RefundRequest.objects.create(
                user=user,
                order=order
            )
            return True
        except Exception as e:
            return str(e)    