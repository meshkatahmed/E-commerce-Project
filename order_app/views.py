from django.shortcuts import render,get_object_or_404,redirect
#Authentications
from django.contrib.auth.decorators import login_required
#Models
from .models import Cart,Order
from shop_app.models import Product
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
    #Bohubrihi - orders = Order.objects.filter(user=request.user,ordered=False)
    if carts.exists():#Bohubrihi - and orders.exists():
        #Bohubrihi - order = orders[0]
        diction = {'carts':carts}##Bohubrihi - ,'order':order}
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
