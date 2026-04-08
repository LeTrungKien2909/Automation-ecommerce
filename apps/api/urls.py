from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'service-types', views.ServiceTypeViewSet)
router.register(r'service-requests', views.ServiceRequestViewSet, basename='servicerequest')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
