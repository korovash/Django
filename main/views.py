from django.db.models import F
from django.db.models.functions import TruncDate
from .models import Device, DeviceDetail
from .forms import DeviceForm
from .filters import DeviceFilter
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django_filters.views import FilterView
from .forms import CsvModelForm
from .models import Csv
from docxtpl import DocxTemplate
import csv
import os
import io
from django.http import FileResponse, HttpResponse
from printmon.settings import BASE_DIR, MEDIA_ROOT

""" Device """

class DeviceIndexView(FilterView):
    model = Device
    template_name = 'main/index.html'
    context_object_name = 'devices'
    paginate_by = 10
    filterset_class = DeviceFilter
    
    def get_context_data(self, *args, **kwargs):
        context = super(DeviceIndexView, self).get_context_data(*args, **kwargs)
        locations = (Device.objects.all()\
                        .values("location")\
                        .order_by('location')\
                        .distinct('location'))

        context['locations'] = locations
        
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)

class DeviceCreateView(CreateView):
    model = Device
    template_name = 'main/create.html'
    form_class = DeviceForm
    success_url = reverse_lazy('main')
    
    def get_context_data(self, *args, **kwargs):
        context = super(DeviceCreateView, self).get_context_data(*args, **kwargs)
        locations = (Device.objects.all()\
                        .values("location")\
                        .order_by('location')\
                        .distinct('location'))
        context['locations'] = locations
        return context

class DeviceEditView(UpdateView):
    model = Device
    template_name = 'main/edit.html'
    form_class = DeviceForm
    success_url = reverse_lazy('main')

    def get_context_data(self, *args, **kwargs):
        context = super(DeviceEditView, self).get_context_data(*args, **kwargs)
        locations = (Device.objects.all()\
                        .values("location")\
                        .order_by('location')\
                        .distinct('location'))
        context['locations'] = locations
        return context


class DeviceDeleteView(DeleteView):
    model = Device
    template_name = 'main/edit.html'
    success_url = reverse_lazy('main')

class DeviceDetailView(ListView):
    model = DeviceDetail
    template_name = 'main/devdetail.html'
    context_object_name = 'device_detail'

    def get_queryset(self):
        return DeviceDetail.objects.filter(device=self.request.resolver_match.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        context = super(DeviceDetailView, self).get_context_data(*args, **kwargs)
        all_print_cnt_by_date = DeviceDetail.objects.all() \
            .annotate(date_item=TruncDate('update_date')) \
            .values("date_item", "printed_count", "black_tonerlevel",
                    "cyan_tonerlevel", "mag_tonerlevel", "yel_tonerlevel") \
            .annotate(printed_item=F("printed_count")) \
            .annotate(black_item=F("black_tonerlevel")) \
            .annotate(cyan_item=F("cyan_tonerlevel")) \
            .annotate(mag_item=F("mag_tonerlevel")) \
            .annotate(yel_item=F("yel_tonerlevel")) \
            .order_by("date_item") \
            .filter(device=self.request.resolver_match.kwargs['pk'])

        date_list = list()
        all_print_cnt_by_date_dict = dict()
        black_cart_by_date_dict = dict()
        cyan_cart_by_date_dict = dict()
        mag_cart_by_date_dict = dict()
        yel_cart_by_date_dict = dict()

        for print_cnt_by_date in all_print_cnt_by_date:
            if not print_cnt_by_date["date_item"].strftime('%d.%m.%Y') in date_list:
                date_list.append(print_cnt_by_date["date_item"].strftime('%d.%m.%Y'))

            if print_cnt_by_date["date_item"].strftime('%d.%m.%Y') in all_print_cnt_by_date:
                all_print_cnt_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')]\
                    += print_cnt_by_date["printed_count"]

                black_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')] \
                    += print_cnt_by_date["black_tonerlevel"]
                cyan_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')] \
                    += print_cnt_by_date["cyan_tonerlevel"]
                mag_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')] \
                    += print_cnt_by_date["mag_tonerlevel"]
                yel_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')] \
                    += print_cnt_by_date["yel_tonerlevel"]
            else:
                all_print_cnt_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')]\
                    = print_cnt_by_date["printed_count"] 

                black_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')]\
                    = print_cnt_by_date["black_tonerlevel"]
                cyan_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')] \
                    = print_cnt_by_date["cyan_tonerlevel"]
                mag_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')] \
                    = print_cnt_by_date["mag_tonerlevel"]
                yel_cart_by_date_dict[print_cnt_by_date["date_item"].strftime('%d.%m.%Y')] \
                    = print_cnt_by_date["yel_tonerlevel"]

        all_print_cnt_by_date_list = list()
        black_cart_list = list()
        cyan_cart_list = list()
        mag_cart_list = list()
        yel_cart_list = list()

        for date_item in date_list:
            if date_item in all_print_cnt_by_date_dict:
                all_print_cnt_by_date_list.append(all_print_cnt_by_date_dict[date_item])
                black_cart_list.append(black_cart_by_date_dict[date_item])
                if cyan_cart_by_date_dict[date_item]:
                    cyan_cart_list.append(cyan_cart_by_date_dict[date_item])
                if mag_cart_by_date_dict[date_item]:
                    mag_cart_list.append(mag_cart_by_date_dict[date_item])
                if yel_cart_by_date_dict[date_item]:
                    yel_cart_list.append(yel_cart_by_date_dict[date_item])

        print_per_day_list = [0]
        for i in range(0, len(all_print_cnt_by_date_list) - 1):
            print_per_day_list.append(all_print_cnt_by_date_list[i+1] - all_print_cnt_by_date_list[i])
        
        charts_data = dict()
        cart_charts_data = dict()
        charts_data["chart_printed"] = dict()
        charts_data["chart_printed"]["date_list"] = date_list
        charts_data["chart_printed"]["series"] = [
            {"name": "Количество отпечатанных страниц", "color": "white", "data": print_per_day_list},
        ]

        cart_charts_data["cart_charts"] = dict()
        cart_charts_data["cart_charts"]["date_list"] = date_list
        cart_charts_data["cart_charts"]["series"] = [
            {"name": "Черный картридж", "color": "black", "data": black_cart_list},
            {"name": "Голубой картридж", "color": "cyan", "data": cyan_cart_list},
            {"name": "Малиновый картридж", "color": "magenta", "data": mag_cart_list},
            {"name": "Желтый картридж", "color": "yellow", "data": yel_cart_list},
        ]

        context['cart_charts'] = cart_charts_data
        context['charts_data'] = charts_data
        return context

def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    success_rows_count = -1
    error_list = list()

    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        success_rows_count += 1
        with open(obj.file_name.path, "r", encoding = "cp1251") as f:
            try:
                reader = csv.reader(f, delimiter=';')
                for i, row in enumerate(reader):
                    if i == 0:
                        pass
                    else:
                        hostname = row[0]
                        inv_num = row[1]
                        location = row[2]
                        desc = row[3]
                        try:
                            Device.objects.create(
                                hostname=hostname,
                                inv_num=inv_num,
                                location=location,
                                desc=desc,
                            )
                            success_rows_count += 1
                        except Exception as error:
                            error_msg = "### Строка {} : {} не будет добавлена по причине: \n{}".format(i, str(row), error)
                            error_list.append(error_msg)
                            pass
            except Exception as error:
                error_msg = "### Проблема с чтением файла: \n{}".format(error)
                error_list.append(error_msg)
            finally:
                obj.activated = True
                obj.save()

    return render(request, 'main/upload.html', {'form': form, 'success_rows_count': success_rows_count, 'error_list': error_list})
