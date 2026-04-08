from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import User, UserProfile
from apps.users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:list')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('users:login')
        else:
            messages.error(request, 'Có lỗi xảy ra, vui lòng kiểm tra lại.')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:list')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Chào mừng, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'products:list')
                return redirect(next_url)
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('users:login')


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')
            user.phone = form.cleaned_data.get('phone', '')
            user.address = form.cleaned_data.get('address', '')
            user.city = form.cleaned_data.get('city', '')
            user.save()
            profile.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    return render(request, 'users/profile.html', {'form': form, 'profile': profile})


@login_required
def dashboard_view(request):
    from apps.orders.models import Order
    from apps.maintenance.models import ServiceRequest
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_service_requests = ServiceRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'recent_orders': recent_orders,
        'recent_service_requests': recent_service_requests,
    }
    return render(request, 'users/dashboard.html', context)
