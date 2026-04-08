from django.urls import path
from apps.maintenance import views

app_name = 'maintenance'

urlpatterns = [
    path('create/', views.service_request_create, name='create'),
    path('list/', views.service_request_list, name='list'),
    path('<int:pk>/', views.service_request_detail, name='detail'),
]
