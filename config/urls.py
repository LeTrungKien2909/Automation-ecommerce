from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def home_redirect(request):
    return redirect('products:list')


urlpatterns = [
    path('', include('apps.users.urls', namespace='users')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('maintenance/', include('apps.maintenance.urls', namespace='maintenance')),
    path('api/', include('apps.api.urls', namespace='api')),
    path('admin/', admin.site.urls),
    path('home/', home_redirect),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
