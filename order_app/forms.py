from django import forms

class CouponForm(forms.Form):
    code = forms.CharField(max_length=10)

    def match_code(self):
        cleaned_data = super().clean()
        if cleaned_data['code']=='xxx':
            return True
        return False
