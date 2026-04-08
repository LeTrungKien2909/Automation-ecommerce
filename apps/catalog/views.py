from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(parent=None)[:6]
    return render(request, 'catalog/home.html', {
        'featured_products': featured_products,
        'categories': categories,
    })


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(parent=None)

    category_slug = request.GET.get('category')
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand = request.GET.get('brand')
    condition = request.GET.get('condition')

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(Q(category=selected_category) | Q(category__parent=selected_category))

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(sku__icontains=query)
        )

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand:
        products = products.filter(brand__icontains=brand)
    if condition:
        products = products.filter(condition=condition)

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })
