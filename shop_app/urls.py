from django.urls import path
#Import views
from . import views


app_name = 'shop_app'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('productdetails/<pk>/',views.ProductDetails.as_view(),name='productdetails'),
    path('productupload/',views.ProductUpload.as_view(),name='productupload'),
]
