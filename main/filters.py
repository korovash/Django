import django_filters
from django.forms import Select
from .models import *


class DeviceFilter(django_filters.FilterSet):
    class Meta:
        model = Device
        fields = ['hostname', 'name', 'ipaddr', 'inv_num', 'location', 'desc', ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

