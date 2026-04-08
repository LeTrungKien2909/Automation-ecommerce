from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from apps.products.models import Category, ProductReview


class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Tìm kiếm', widget=forms.TextInput(attrs={'placeholder': 'Tên sản phẩm...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Danh mục', empty_label='Tất cả danh mục')
    min_price = forms.DecimalField(required=False, label='Giá từ', min_value=0)
    max_price = forms.DecimalField(required=False, label='Giá đến', min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('q', css_class='col-md-4'),
                Column('category', css_class='col-md-3'),
                Column('min_price', css_class='col-md-2'),
                Column('max_price', css_class='col-md-2'),
                Column(Submit('submit', 'Tìm', css_class='btn btn-primary mt-4'), css_class='col-md-1'),
            )
        )


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Đánh giá',
            'comment': 'Nhận xét',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rating',
            'comment',
            Submit('submit', 'Gửi đánh giá', css_class='btn btn-primary'),
        )
