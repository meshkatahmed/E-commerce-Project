from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404,redirect
#Decorators and mixins
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#Class-based views
from django.views.generic import FormView
#Models and forms
from .models import Cart,Order
from shop_app.models import Product
from .forms import CouponForm
#Messages
from django.contrib import messages
# Create your views here.
@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_item = Cart.objects.get_or_create(item=item,user=request.user,purchased=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request,"This item's quantity is updated")
            return redirect('shop_app:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request,"This item is added to your cart")
            return redirect('shop_app:home')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request,"This item is added to your cart")
        return redirect('shop_app:home')

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)
    orders = Order.objects.filter(user=request.user,ordered=False)
    if carts.exists():#Bohubrihi - and orders.exists():
        order = orders[0]
        diction = {'carts':carts,'order':order}
        return render(request,'order_app/cart.html',context=diction)
    else:
        messages.warning(request,"You don't have any item in your cart!")
        return redirect('shop_app:home')

@login_required
def remove_from_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            items_to_remove = Cart.objects.filter(item=item,user=request.user,purchased=False)
            item_to_remove = items_to_remove[0]
            order.orderitems.remove(item_to_remove)
            item_to_remove.delete()
            messages.warning(request,"This item is removed from your cart")
            return redirect('order_app:cart')
        else:
            messages.info(request,"This item is not available in your cart")
            return redirect('shop_app:home')
    else:
        messages.info(request,"You don't have an active order")
        return redirect('shop_app:home')

@login_required
def increase_quantity(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            items_to_increase_quantity = Cart.objects.filter(item=item,user=request.user,purchased=False)
            item_to_increase_quantity = items_to_increase_quantity[0]
            if item_to_increase_quantity.quantity >= 1:
                item_to_increase_quantity.quantity += 1
                item_to_increase_quantity.save()
                return redirect('order_app:cart')
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect('order_app:cart')
    else:
        messages.info(request,"You don't have an active order")
        return redirect('shop_app:home')
@login_required
def decrease_quantity(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            items_to_decrease_quantity = Cart.objects.filter(item=item,user=request.user,purchased=False)
            item_to_decrease_quantity = items_to_decrease_quantity[0]
            if item_to_decrease_quantity.quantity > 1:
                item_to_decrease_quantity.quantity -= 1
                item_to_decrease_quantity.save()
                return redirect('order_app:cart')
            else:
                order.orderitems.remove(item_to_decrease_quantity)
                item_to_decrease_quantity.delete()
                messages.warning(request, f"{item.name} is removed form your cart")
                return redirect('order_app:cart')
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect('order_app:cart')
    else:
        messages.info(request,"You don't have an active order")
        return redirect('shop_app:home')

class ApplyCoupon(LoginRequiredMixin,FormView):
    form_class = CouponForm
    template_name = 'order_app/applycoupon.html'

    def form_valid(self,form):
        if form.match_code():
            return redirect('order_app:couponmatchedcart')
        return redirect('order_app:couponunmatchedcart')

@login_required
def coupon_matched_cart(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)

    if carts.exists():
        messages.success(request,'Coupon code matched!!')
        active_orders = Order.objects.filter(user=request.user,ordered=False)
        diction = {'carts':carts,'order':active_orders[0],'get_discount':True}
        return render(request,'order_app/cart.html',context=diction)
    messages.warning(request,"You don't have an active order!!")
    return redirect('shop_app:home')

@login_required
def coupon_unmatched_cart(request):
    messages.info(request,'Coupon code not matched!!')
    return redirect('order_app:cart')
