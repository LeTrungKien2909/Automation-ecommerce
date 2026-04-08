from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('request/', views.create_service_request, name='create_request'),
    path('my-requests/', views.my_service_requests, name='my_requests'),
    path('my-requests/<int:pk>/', views.service_request_detail, name='request_detail'),
    path('maintenance/', views.maintenance_schedule, name='maintenance_schedule'),
]
