from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.orders.models import Cart, CartItem, Order, OrderItem
from apps.products.models import Product
from apps.orders.forms import CheckoutForm


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, session_key='')
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)
    return cart


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    return render(request, 'orders/cart.html', {'cart': cart, 'items': items})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Đã thêm "{product.name}" vào giỏ hàng!')
        return redirect('orders:cart')
    return redirect('products:list')


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, pk=item_id)
        cart = get_or_create_cart(request)
        if item.cart == cart:
            item.delete()
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('orders:cart')


def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(pk=item_id, cart=cart)
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
        except CartItem.DoesNotExist:
            pass
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'total': str(cart.total)})
    return redirect('orders:cart')


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    if not items:
        messages.warning(request, 'Giỏ hàng của bạn đang trống.')
        return redirect('orders:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            shipping_address = f"{data['shipping_address']}, {data['city']}"
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total,
                shipping_address=shipping_address,
                phone=data['phone'],
                notes=data.get('notes', ''),
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.effective_price,
                )
            cart.items.all().delete()
            messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: {order.order_number}')
            return redirect('orders:order_detail', order_number=order.order_number)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.phone,
                'shipping_address': request.user.address,
                'city': request.user.city,
            }
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart, 'items': items})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    items = order.items.select_related('product').all()
    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})
