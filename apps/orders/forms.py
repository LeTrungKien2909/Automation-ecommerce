from django import forms


class CheckoutForm(forms.Form):
    shipping_name = forms.CharField(max_length=200, label='Full Name')
    shipping_email = forms.EmailField(label='Email')
    shipping_phone = forms.CharField(max_length=20, label='Phone')
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Address')
    shipping_city = forms.CharField(max_length=100, label='City')
    shipping_country = forms.CharField(max_length=100, label='Country')
    shipping_postal_code = forms.CharField(max_length=20, label='Postal Code')
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Order Notes')
