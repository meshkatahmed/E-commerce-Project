from django.urls import path
from . import views
app_name = 'order_app'

urlpatterns = [
    path('addtocart/<pk>/',views.add_to_cart,name='addtocart'),
    path('cart/',views.cart_view,name='cart'),
    path('removefromcart/<pk>',views.remove_from_cart,name='removefromcart'),
]
