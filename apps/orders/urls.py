from django.urls import path
from apps.orders import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('list/', views.order_list, name='order_list'),
    path('<str:order_number>/', views.order_detail, name='order_detail'),
]
