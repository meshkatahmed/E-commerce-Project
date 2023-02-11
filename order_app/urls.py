from django.urls import path
from . import views
app_name = 'order_app'

urlpatterns = [
    path('addtocart/<pk>/',views.add_to_cart,name='addtocart'),
    path('cart/',views.cart_view,name='cart'),
    path('removefromcart/<pk>/',views.remove_from_cart,name='removefromcart'),
    path('increasequantity/<pk>/',views.increase_quantity,name='increasequantity'),
    path('decreasequantity/<pk>/',views.decrease_quantity,name='decreasequantity'),
    path('applycoupon/',views.ApplyCoupon.as_view(),name='applycoupon'),
    path('couponmatchedcart/',views.coupon_matched_cart,name='couponmatchedcart'),
    path('couponunmatchedcart/',views.coupon_unmatched_cart,name='couponunmatchedcart'),
]
