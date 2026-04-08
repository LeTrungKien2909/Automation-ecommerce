from rest_framework import serializers
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem
from apps.services.models import ServiceType, ServiceRequest


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    effective_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'sku', 'description', 'price', 'discount_price',
                  'effective_price', 'stock', 'brand', 'condition', 'category', 'category_name',
                  'is_active', 'is_featured', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_sku', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'total', 'created_at', 'items']


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'description', 'price_per_hour']


class ServiceRequestSerializer(serializers.ModelSerializer):
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)

    class Meta:
        model = ServiceRequest
        fields = ['id', 'title', 'description', 'priority', 'status', 'service_type',
                  'service_type_name', 'scheduled_date', 'created_at']
        read_only_fields = ['status']
