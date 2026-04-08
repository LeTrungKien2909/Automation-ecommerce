from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.maintenance.models import ServiceRequest, ServiceCategory
from apps.maintenance.forms import ServiceRequestForm


@login_required
def service_request_create(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            messages.success(request, 'Yêu cầu bảo trì đã được gửi thành công!')
            return redirect('maintenance:list')
        else:
            messages.error(request, 'Có lỗi xảy ra, vui lòng kiểm tra lại.')
    else:
        form = ServiceRequestForm()
    return render(request, 'maintenance/request.html', {'form': form})


@login_required
def service_request_list(request):
    requests = ServiceRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'maintenance/list.html', {'requests': requests})


@login_required
def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
    history = service_request.history.select_related('technician').order_by('date')
    return render(request, 'maintenance/detail.html', {
        'service_request': service_request,
        'history': history,
    })
