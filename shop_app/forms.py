from django import forms
from . import models

#Forms
class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
