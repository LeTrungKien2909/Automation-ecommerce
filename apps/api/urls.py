from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.api import views

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'service-requests', views.ServiceRequestViewSet, basename='service-request')
router.register(r'cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
