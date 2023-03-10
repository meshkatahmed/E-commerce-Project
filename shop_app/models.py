from django.db import models
from django.conf import settings
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    mainimage = models.ImageField(upload_to='products',blank=True)
    name = models.CharField(max_length=264)
    seller_name = models.CharField(max_length=264)
    seller_phone = models.CharField(max_length=20,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    preview_text = models.TextField(max_length=200,verbose_name='Preview Text')
    detailed_text = models.TextField(max_length=1000,verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created_at = models. DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at',]
