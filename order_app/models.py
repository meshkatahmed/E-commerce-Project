from django.db import models
from django.conf import settings
#Models
from shop_app.models import Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
    related_name="cart")
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} x {self.item}'

    def get_total(self):
        total =  self.item.price * self.quantity
        float_total = format(total,'0.2f')
        return float_total
