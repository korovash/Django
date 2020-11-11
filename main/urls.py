from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import upload_file_view
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.DeviceIndexView.as_view(), name='main'),
    path('create/', views.DeviceCreateView.as_view(), name='create'),
    path('upload/', upload_file_view, name='upload'),
    path('edit/<int:pk>', views.DeviceEditView.as_view(), name='edit'),
    path('delete/<int:pk>', views.DeviceDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>', views.DeviceDetailView.as_view(), name='detail'),
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
