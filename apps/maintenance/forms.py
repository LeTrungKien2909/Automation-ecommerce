from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from apps.maintenance.models import ServiceRequest, ServiceCategory
from apps.products.models import Product


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'service_category', 'priority', 'product', 'notes']
        labels = {
            'title': 'Tiêu đề',
            'description': 'Mô tả yêu cầu',
            'service_category': 'Loại dịch vụ',
            'priority': 'Mức độ ưu tiên',
            'product': 'Thiết bị (nếu có)',
            'notes': 'Ghi chú thêm',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = False
        self.fields['product'].queryset = Product.objects.filter(is_active=True)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Row(
                Column('service_category', css_class='col-md-6'),
                Column('priority', css_class='col-md-6'),
            ),
            'product',
            'description',
            'notes',
            Submit('submit', 'Gửi yêu cầu', css_class='btn btn-primary'),
        )
