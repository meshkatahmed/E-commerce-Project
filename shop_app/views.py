from django.shortcuts import render,redirect
from django.contrib import messages
#Import Base Class Based views
from django.views.generic import ListView,DetailView,FormView
#Import models & forms
from .models import Product
from .forms import ProductForm
#Decorators and Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'shop_app/home.html'

class ProductDetails(LoginRequiredMixin,DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop_app/productdetails.html'

class ProductUpload(LoginRequiredMixin,FormView):
    form_class = ProductForm
    template_name = 'shop_app/productupload.html'

    def form_valid(self,form):
        form.save()
        return redirect('shop_app:home')
