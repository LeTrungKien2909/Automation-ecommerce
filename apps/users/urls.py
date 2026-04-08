from django.urls import path
from apps.users import views

app_name = 'users'

urlpatterns = [
    path('users/login/', views.login_view, name='login'),
    path('users/logout/', views.logout_view, name='logout'),
    path('users/register/', views.register_view, name='register'),
    path('users/profile/', views.profile_view, name='profile'),
    path('users/dashboard/', views.dashboard_view, name='dashboard'),
]
