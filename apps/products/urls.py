from django.urls import path
from apps.products import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('search/', views.product_search, name='search'),
    path('categories/', views.category_list, name='categories'),
    path('category/<slug:slug>/', views.product_list, name='by_category'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('review/<int:pk>/', views.add_review, name='add_review'),
]
