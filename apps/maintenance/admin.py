from django.contrib import admin
from apps.maintenance.models import ServiceCategory, ServiceRequest, ServiceHistory


class ServiceHistoryInline(admin.TabularInline):
    model = ServiceHistory
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'service_category', 'status', 'priority', 'assigned_staff', 'created_at']
    list_filter = ['status', 'priority', 'service_category']
    search_fields = ['title', 'user__username']
    list_editable = ['status', 'assigned_staff']
    ordering = ['-created_at']
    inlines = [ServiceHistoryInline]
