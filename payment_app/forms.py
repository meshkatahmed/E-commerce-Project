from django import forms
from .models import BillingAddress

#Forms
class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address','zipcode','city','country']
