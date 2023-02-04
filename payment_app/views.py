from django.shortcuts import render,redirect
from django.urls import reverse
#Models and Forms
from order_app.models import Order
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

# Create your views here.
@login_required
def checkout(request):
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
    print(order_qs)
    order_items = order_qs[0].orderitems.all()
    print(order_items)
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

@login_required
def complete(request):
    diction = {}
    return render(request,'payment_app/complete.html',context=diction)
