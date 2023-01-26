from django.urls import path
#Import views
from . import views
app_name = 'shop_app'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
]
