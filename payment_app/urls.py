from django.urls import path
from . import views

app_name = 'payment_app'

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('makepayment/',views.payment,name='makepayment'),
    path('status/',views.complete,name='complete'),
    path('purchase/<val_id>/<tran_id>/',views.purchase,name='purchase'),
    path('orders/',views.order_view,name='orders'),
]
