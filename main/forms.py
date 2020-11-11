from .models import Device
from django.forms import ModelForm, TextInput, Select, Textarea
from django import forms


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ["hostname", "inv_num", "location", "desc"]
        error_messages = {
            "inv_num": {
                'unique': "Такой инв. номер уже существует в БД",
            },
        }
        widgets = {
            "hostname": TextInput(attrs={
                'class': 'text-input',
                'placeholder': 'Введите сетевое имя или IP-адрес',
            }),
            "inv_num": TextInput(attrs={
                'class': 'text-input',
                'placeholder': 'Введите инвентарный номер (15 цифр)',
            }),
            "location": TextInput(attrs={
                'class': 'text-input',
                'placeholder': 'Введите расположение',
                'outline': 'none',
                'list': 'locations'
            }),
            "desc": Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'Введите описание',
                'cols': '50',
                'id': 'desc',
                'rows': '4',
            }),
        }
        required = False

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = "Выберете расположение"

from .models import Csv


class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',)
