from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from apps.users.models import User, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=20, required=False, label='Số điện thoại')
    first_name = forms.CharField(max_length=150, required=True, label='Họ')
    last_name = forms.CharField(max_length=150, required=True, label='Tên')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'username',
            'email',
            'phone',
            'password1',
            'password2',
            Submit('submit', 'Đăng ký', css_class='btn btn-primary w-100 mt-2'),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập')
    password = forms.CharField(widget=forms.PasswordInput, label='Mật khẩu')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Đăng nhập', css_class='btn btn-primary w-100 mt-2'),
        )


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False, label='Họ')
    last_name = forms.CharField(max_length=150, required=False, label='Tên')
    email = forms.EmailField(required=False, label='Email')
    phone = forms.CharField(max_length=20, required=False, label='Số điện thoại')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Địa chỉ')
    city = forms.CharField(max_length=100, required=False, label='Thành phố')

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'company', 'tax_code']
        labels = {
            'avatar': 'Ảnh đại diện',
            'bio': 'Giới thiệu',
            'company': 'Công ty',
            'tax_code': 'Mã số thuế',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.phone
            self.fields['address'].initial = user.address
            self.fields['city'].initial = user.city
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'email',
            Row(
                Column('phone', css_class='col-md-6'),
                Column('city', css_class='col-md-6'),
            ),
            'address',
            'company',
            'tax_code',
            'bio',
            'avatar',
            Submit('submit', 'Cập nhật', css_class='btn btn-primary mt-2'),
        )
