# /supermarket/suppliers/models.py
from django.db import models

class Supplier(models.Model):
    """供应商表"""
    supplier_name = models.CharField(max_length=100, verbose_name='供应商名称')
    contact_person = models.CharField(max_length=50, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=11, blank=True, verbose_name='电话')
    address = models.CharField(max_length=200, blank=True, verbose_name='地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = '供应商'
        ordering = ['-create_time']

    def __str__(self):
        return self.supplier_name
# Create your models here.
