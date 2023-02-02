from django.shortcuts import render
#Models and Forms
from order_app.models import Order
from .models import BillingAddress
from .forms import BillingForm
#Decorators
from django.contrib.auth.decorators import login_required
#Messages
from django.contrib import messages

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
    diction = {'form':form,'order_items':order_items,'order_total':order_total}
    return render(request,'payment_app/checkout.html',context=diction)
