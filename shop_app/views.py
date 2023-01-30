from django.shortcuts import render
#Import Base Class Based views
from django.views.generic import ListView,DetailView
#Import models
from .models import Product
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
