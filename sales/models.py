# /supermarket/sales/models.py
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class SalesOrder(models.Model):
    """销售单主表"""
    ORDER_STATUS = (
        (0, '已创建'),
        (1, '已结算'),
        (2, '部分退货'),
        (3, '全部退货'),
    )
    order_code = models.CharField(max_length=20, unique=True, verbose_name='销售单号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    actual_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实收金额')
    cashier = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_orders', verbose_name='收银员')
    status = models.SmallIntegerField(choices=ORDER_STATUS, default=0, verbose_name='状态')

    class Meta:
        verbose_name = '销售单'
        verbose_name_plural = '销售单'
        ordering = ['-create_time']

    def __str__(self):
        return self.order_code

class SalesOrderItem(models.Model):
    """销售单明细"""
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items', verbose_name='销售单')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='商品')
    sales_quantity = models.IntegerField(verbose_name='销售数量')
    sell_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='销售价')
    return_quantity = models.IntegerField(default=0, verbose_name='退货数量')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')

    class Meta:
        verbose_name = '销售单明细'
        verbose_name_plural = '销售单明细'

    def __str__(self):
        return f'{self.order.order_code} - {self.product.product_name}'
# Create your models here.
