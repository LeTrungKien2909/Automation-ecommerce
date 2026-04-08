from .models import Cart


def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.item_count
        except Cart.DoesNotExist:
            pass
    elif hasattr(request, 'session') and request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            count = cart.item_count
        except Cart.DoesNotExist:
            pass
    return {'cart_count': count}
