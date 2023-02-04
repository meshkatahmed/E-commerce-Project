from django.urls import path
from . import views

app_name = 'payment_app'

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('makepayment/',views.payment,name='makepayment'),
    path('status/',views.complete,name='complete'),
]
