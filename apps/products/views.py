from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apps.products.models import Category, Product, ProductReview
from apps.products.forms import ProductSearchForm, ProductReviewForm


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()
    form = ProductSearchForm(request.GET)

    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None

    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except (InvalidOperation, ValueError):
            pass
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            pass

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'form': form,
        'current_category': category,
        'q': q,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.select_related('user').order_by('-created_at')
    review_form = ProductReviewForm()
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'related_products': related_products,
    }
    return render(request, 'products/detail.html', context)


def category_list(request):
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    return render(request, 'products/categories.html', {'categories': categories})


def product_search(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'products/search.html', {'page_obj': page_obj, 'q': q})


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            existing = ProductReview.objects.filter(product=product, user=request.user).first()
            if existing:
                messages.warning(request, 'Bạn đã đánh giá sản phẩm này rồi.')
            else:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Đánh giá của bạn đã được ghi nhận!')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại đánh giá.')
    return redirect('products:detail', slug=product.slug)
