from django.shortcuts import render,redirect
from django.contrib import messages
#Import Base Class Based views
from django.views.generic import ListView,DetailView,CreateView
#Import models & forms
from .models import Product
#Decorators and Mixins
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'shop_app/home.html'

class ProductDetails(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop_app/productdetails.html'

class ProductUpload(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['mainimage','name','category','preview_text','detailed_text','price','old_price']
    template_name = 'shop_app/productupload.html'

    def form_valid(self,form):
        form_obj = form.save(commit=False)
        form_obj.seller_name = self.request.user.profile.full_name
        form_obj.seller_phone = self.request.user.profile.phone
        form_obj.save()
        return redirect('shop_app:home')
