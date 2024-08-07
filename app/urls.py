from django.urls import path

from .views import *

from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('delete_device/<int:device_id>/', delete_device, name='delete_device'),
    path('home/', lambda request: render(request, "home.html"), name='home'),
    path('add_device/', add_device, name='add_device'),
    path('delete/<int:device_id>/', delete_device, name='delete_device'),
    path('success/', lambda request: render(request, 'success.html'), name='success'),
    path('export-excel/', export_to_excel, name='export_excel'),
    path('query/', query, name="query"),
    path('results/', results, name="results"),
    path('ajax/load-districts/', load_districts, name='ajax_load_districts'),
    path('ajax/load-models/', load_models, name='ajax_load_models'),
    path('trash/', trash_list, name='trash_list'),
    path('restore_device/<int:device_id>/', restore_device, name='restore_device'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update-device/<int:device_id>/', update_device, name='update_device'), 
    path('add_user/', add_user, name='add_user'),
    path('edit_users/', edit_users, name='edit_users'),
    path('update-user-role/<int:user_id>/', update_user_role, name='update_user_role'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
