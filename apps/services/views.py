from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceRequest, ServiceType, MaintenanceSchedule
from .forms import ServiceRequestForm, MaintenanceScheduleForm


def service_list(request):
    service_types = ServiceType.objects.filter(is_active=True)
    return render(request, 'services/service_list.html', {'service_types': service_types})


@login_required
def create_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            messages.success(request, 'Service request submitted successfully!')
            return redirect('services:my_requests')
    else:
        form = ServiceRequestForm()
    return render(request, 'services/create_request.html', {'form': form})


@login_required
def my_service_requests(request):
    requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'services/my_requests.html', {'service_requests': requests})


@login_required
def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
    return render(request, 'services/request_detail.html', {'service_request': service_request})


@login_required
def maintenance_schedule(request):
    schedules = MaintenanceSchedule.objects.filter(user=request.user, is_active=True)
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            messages.success(request, 'Maintenance schedule created!')
            return redirect('services:maintenance_schedule')
    else:
        form = MaintenanceScheduleForm()
    return render(request, 'services/maintenance_schedule.html', {'form': form, 'schedules': schedules})
