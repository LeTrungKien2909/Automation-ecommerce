from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên loại dịch vụ')
    description = models.TextField(blank=True, verbose_name='Mô tả')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Loại dịch vụ'
        verbose_name_plural = 'Loại dịch vụ'


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('assigned', 'Đã phân công'),
        ('in_progress', 'Đang thực hiện'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='service_requests', verbose_name='Khách hàng')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Thiết bị')
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, verbose_name='Loại dịch vụ')
    title = models.CharField(max_length=300, verbose_name='Tiêu đề')
    description = models.TextField(verbose_name='Mô tả yêu cầu')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Trạng thái')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='Ưu tiên')
    assigned_staff = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_requests', verbose_name='Nhân viên phụ trách'
    )
    requested_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True, verbose_name='Ngày hẹn')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='Ngày hoàn thành')
    notes = models.TextField(blank=True, verbose_name='Ghi chú')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Yêu cầu bảo trì'
        verbose_name_plural = 'Yêu cầu bảo trì'
        ordering = ['-created_at']


class ServiceHistory(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='history')
    technician = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='Kỹ thuật viên')
    work_done = models.TextField(verbose_name='Công việc đã thực hiện')
    materials_used = models.TextField(blank=True, verbose_name='Vật tư sử dụng')
    cost = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Chi phí')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History for {self.service_request.title}'

    class Meta:
        verbose_name = 'Lịch sử bảo trì'
