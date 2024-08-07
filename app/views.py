import os

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl import Workbook
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import *
from .models import *

@login_required
def update_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('results')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'update_device.html', {'form': form, 'device': device})

@login_required
def load_districts(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'district_dropdown_list_options.html', {'districts': districts})

@login_required
def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = Router.objects.filter(brand_id=brand_id).order_by('model_name')
    return render(request, 'model_dropdown_list_options.html', {'models': models})

@login_required
def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to another page after saving
    else:
        form = DeviceForm()
    return render(request, 'add_device.html', {'form': form})


@login_required
def add_user(request):
    if not request.user.is_staff:
        return render(request, 'no_permission.html') 
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            if user_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.save()
            messages.success(request, f'User {user.username} has been created successfully!')
            return render(request, 'user_created_success.html', {'username': user.username})
    else:
        form = UserRegistrationForm()
    return render(request, 'add_user.html', {'form': form})

@login_required
def edit_users(request):
    if not request.user.is_staff:
        return render(request, 'no_permission.html')
    
    users = User.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, f'User {user.username} has been deleted successfully!')
        return redirect('edit_users')
    
    return render(request, 'edit_users.html', {'users': users})

@login_required
def update_user_role(request, user_id):
    if not request.user.is_staff:
        return render(request, 'no_permission.html') 
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()
        messages.success(request, f'User {user.username} role updated to {role.capitalize()}!')
    
    return redirect('edit_users')

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return render(request, 'no_permission.html') 
    
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.username} has been deleted successfully!')
        return redirect('edit_users')

    return redirect('edit_users')

@require_POST
@login_required
def delete_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device.deleted = True
    device.save()
    
    # Add the device to the Trash table
    Trash.objects.create(device=device)
    
    return redirect(reverse('results'))

@login_required
def restore_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device.deleted = False
    device.save()
    return redirect(reverse('trash_list'))

@login_required
def trash_list(request):
    devices = Device.objects.filter(deleted=True)
    return render(request, 'trash_list.html', {'devices': devices})

@login_required
def query(request):
    devices = Device.objects.filter(deleted=False)
    provinces = Province.objects.all()
    return render(request, 'query.html', {'devices': devices, 'provinces': provinces})

@login_required
def results(request):
    province_id = request.GET.get('province')
    devices = Device.objects.filter(province_id=province_id) if province_id else Device.objects.filter(deleted=False)
    return render(request, 'results.html', {'devices': devices})

@login_required
def export_to_excel(request):
    # Query to get all Device records from the database
    telekom_data = Device.objects.all()

    # Create a new Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Telekom Data"

    # Write the headers to the first row
    headers = [
        'Şehir', 'İlçe', 'Santral Bina', 'Lokasyon', 'Router', 'Adet',
        'Port Sayısı', 'Bağlı Cihaz / Port', 'Bağlı Cihaz Lokasyon',
        'Loopback IP', 'VLAN', 'Bağlantı', 'Enerji', 'Temos'
    ]
    ws.append(headers)

    # Write the data to the worksheet
    for data in telekom_data:
        routers_info = ', '.join(
            [f"{router.brand.name} {router.model_name} / {data.connection_port or '?'}" for router in
             data.connected_routers.all()]
        )
        
        ws.append([
            data.province.name if data.province else '',
            data.district.name if data.district else '',
            data.station or '',
            f"{data.location_name or ''} {data.location_floor or ''}",
            f"{data.router_model or ''}",
            data.router_count or '',
            data.number_of_ports or '',
            routers_info,
            data.connected_router_location or '',
            data.loopback_ip or '',
            data.vlan or '',
            data.connection or '',
            data.energy_type or '',
            data.temos or ''
        ])

    # Create an HTTP response with the workbook
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=telekom_data.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response


