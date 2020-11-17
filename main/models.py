from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F
from django.urls import reverse
from .validators.validators import MSG_INV_NUM_NOT_VALID

# Create your models here.


class Device(models.Model):

    hostname = models.CharField('Имя узла', max_length=30)
    name = models.CharField('Название устройства', max_length=200, default='Нет данных', null=True)
    ipaddr = models.CharField('IP адрес', max_length=20, default='Нет данных', null=True)
    status = models.CharField('Состояние', max_length=30, default='Нет данных', null=True)
    inv_num = models.CharField('Инвентарный номер', default="1014000000", null=False, unique=True, max_length=15,
                               validators=[RegexValidator('^[0-9]{15}$', MSG_INV_NUM_NOT_VALID)])
    serial_num = models.CharField('Серийный номер', max_length=50, default='Нет данных', null=True)
    location = models.CharField('Местоположение номер', max_length=150, null=True)
    desc = models.CharField('Описание', default="", max_length=255, blank=True)
    update_date = models.DateTimeField('Дата', null=True)
    
    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
        ordering = ["hostname"]


class DeviceDetail(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="dev_detail")
    update_date = models.DateTimeField('Дата', null=True)
    hostname = models.CharField('Имя узла', max_length=30, null=True)
    printed_count = models.IntegerField('Количество отпечатанных страниц', null=True)
    black_cart_name = models.CharField('Наименование черного картриджа', max_length=150, blank=True, null=True)
    black_tonerlevel = models.IntegerField('Уровень черного тонера', blank=True, null=True)
    cyan_cart_name = models.CharField('Наименование голубого картриджа', max_length=150, blank=True, null=True)
    cyan_tonerlevel = models.IntegerField('Уровень голубого тонера', blank=True, null=True)
    mag_cart_name = models.CharField('Наименование малинового картриджа', max_length=150, blank=True, null=True)
    mag_tonerlevel = models.IntegerField('Уровень малинового тонера', blank=True, null=True)
    yel_cart_name = models.CharField('Наименование желтого картриджа', max_length=150, blank=True, null=True)
    yel_tonerlevel = models.IntegerField('Уровень желтого тонера', blank=True, null=True)

    def __str__(self):
        return str(self.hostname)

    """ def get_absolute_url(self):
            return reverse('detail-view', args=[str(self.pk)]) """

    class Meta:
        ordering = ["-update_date"]

class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.pk}"