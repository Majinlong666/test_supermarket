# /supermarket/products/models.py
from django.db import models
from suppliers.models import Supplier

class Product(models.Model):
    """商品表"""
    product_code = models.CharField(
    max_length=20,
    unique=True,
    verbose_name='商品编码',
    error_messages={
        'unique': '该商品编码已存在！请更换编码',
    }
)
    product_name = models.CharField(max_length=100, verbose_name='商品名称')
    category = models.CharField(max_length=50, blank=True, verbose_name='分类')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products', verbose_name='供应商')
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='采购价')
    sell_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='销售价')
    stock_quantity = models.IntegerField(default=0, verbose_name='库存')
    warning_quantity = models.IntegerField(default=10, verbose_name='预警库存')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-create_time']

    def __str__(self):
        return self.product_name
# Create your models here.
