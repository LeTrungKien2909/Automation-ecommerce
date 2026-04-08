import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cart.views import get_or_create_cart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            subtotal = cart.total
            shipping_cost = 0
            total = subtotal + shipping_cost

            order = Order.objects.create(
                user=request.user,
                order_number=str(uuid.uuid4())[:8].upper(),
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                total=total,
                **{k: v for k, v in form.cleaned_data.items()}
            )

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_sku=cart_item.product.sku,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.effective_price,
                    subtotal=cart_item.subtotal,
                )
                product = cart_item.product
                product.stock = max(0, product.stock - cart_item.quantity)
                product.save()

            cart.items.all().delete()

            messages.success(request, f'Order #{order.order_number} placed successfully!')
            return redirect('orders:order_detail', order_number=order.order_number)
    else:
        profile = getattr(request.user, 'profile', None)
        initial = {}
        if profile:
            initial = {
                'shipping_name': f"{request.user.first_name} {request.user.last_name}",
                'shipping_email': request.user.email,
                'shipping_phone': profile.phone,
                'shipping_address': profile.address,
                'shipping_city': profile.city,
                'shipping_country': profile.country,
                'shipping_postal_code': profile.postal_code,
            }
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
