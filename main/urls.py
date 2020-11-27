from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import upload_file_view, export_table_to_csv
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from cacheops import cached_view_as
from .models import Device

urlpatterns = [
    path('', login_required(cached_view_as(Device)(views.DeviceIndexView.as_view()), login_url='login'), name='main'),
    path('create/', login_required(views.DeviceCreateView.as_view(), login_url='login'), name='create'),
    path('remove/', login_required(views.DeviceIndexView.as_view(), login_url='login'), name='remove'),
    path('upload/', login_required(upload_file_view, login_url='login'), name='upload'),
    path('edit/<int:pk>', login_required(views.DeviceEditView.as_view(), login_url='login'), name='edit'),
    # path('delete/<int:pk>', login_required(views.DeviceDeleteView.as_view(), login_url='login'), name='delete'),
    path('detail/<int:pk>', login_required(views.DeviceDetailView.as_view(), login_url='login'), name='detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('export_csv/', login_required(views.export_table_to_csv, login_url='login'), name='export_data_csv'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)