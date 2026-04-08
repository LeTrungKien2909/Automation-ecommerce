from apps.orders.models import Cart


def cart_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, session_key='').first()
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(user=None, session_key=session_key).first()
            else:
                cart = None
        if cart:
            count = cart.total_items
    except Exception:
        count = 0
    return {'cart_count': count}
