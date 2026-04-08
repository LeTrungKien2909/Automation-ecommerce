from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=150, label='Họ')
    last_name = forms.CharField(max_length=150, label='Tên')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Số điện thoại')
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Địa chỉ giao hàng'
    )
    city = forms.CharField(max_length=100, label='Thành phố')
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Ghi chú'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'email',
            'phone',
            'shipping_address',
            'city',
            'notes',
            Submit('submit', 'Đặt hàng', css_class='btn btn-primary btn-lg w-100 mt-3'),
        )
