from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
#Models and Forms
from order_app.models import Order,Cart
from .models import BillingAddress
from .forms import BillingForm
#Decorators
from django.contrib.auth.decorators import login_required
#Messages
from django.contrib import messages
#For payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def checkout(request,get_discount):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    working_address = saved_address[0]
    form = BillingForm(instance = working_address)

    if request.method=='POST':
        form = BillingForm(request.POST,instance = working_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance = working_address)
            messages.info(request,'Your shipping address is saved!')
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order_items = order_qs[0].orderitems.all()
    if get_discount=='True':
        order_total = order_qs[0].discounted_totals()
    else:
        order_total = order_qs[0].get_totals()
    diction = {'form':form,'order_items':order_items,'order_total':order_total,
    'working_address':working_address}
    return render(request,'payment_app/checkout.html',context=diction)

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    working_address = saved_address[0]

    if not working_address.is_fully_filled():
        messages.info(request,'Please fullfil shipping address!!')
        return redirect('payment_app:checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request,'Please fullfil profile details!!')
        return redirect('login_app:profile')

    store_id = 'mycom63de3e35dfd00'
    API_key = 'mycom63de3e35dfd00@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
    sslc_store_pass=API_key)

    status_url = request.build_absolute_uri(reverse('payment_app:complete'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
    cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT',
    product_category='Mixed', product_name=order_items, num_of_item=order_items_count,
    shipping_method='Courier', product_profile='None')

    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name,
    email=current_user.email, address1=current_user.profile.address,
    address2=current_user.profile.address, city=current_user.profile.city,
    postcode=current_user.profile.zipcode, country=current_user.profile.country,
    phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name,
    address=working_address.address, city=working_address.city,
    postcode=working_address.zipcode, country=working_address.country)

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complete(request):
    if request.method=='POST' or request.method=='post':
         payment_data = request.POST
         status = payment_data['status']

         if status == 'VALID':
             val_id =  payment_data['val_id']
             tran_id = payment_data['tran_id']
             messages.success(request,"Your payment is completed successfully!")
             return HttpResponseRedirect(reverse('payment_app:purchase',
             kwargs={'val_id':val_id,'tran_id':tran_id}))
         elif status == 'FAILED':
             messages.warning(request,'Your payment is failed. Please, try again!')
    diction = {}
    return render(request,'payment_app/complete.html',context=diction)

@login_required
def purchase(request,val_id,tran_id):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.orderId = tran_id
    order.paymentId = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user,purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return redirect('shop_app:home')

@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user,ordered=True)
        diction = {'orders':orders}
    except:
        messages.warning(request,"You didn't order before!!")
        return redirect('shop_app:home')
    return render(request,'payment_app/order.html',context=diction)
