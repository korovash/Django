from django.contrib import admin
from .models import Device, DeviceDetail, Csv

# Register your models here.

admin.site.register(Device)
admin.site.register(DeviceDetail)
admin.site.register(Csv)