from django.contrib import admin
from .models import ServiceType, ServiceRequest, MaintenanceSchedule


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_hour', 'is_active']
    list_editable = ['is_active']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'service_type', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'service_type']
    list_editable = ['status']
    search_fields = ['title', 'user__username']


@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'service_type', 'frequency', 'next_service_date', 'is_active']
    list_filter = ['frequency', 'is_active']
