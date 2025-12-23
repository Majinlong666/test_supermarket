from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
import uuid
from django.core.exceptions import PermissionDenied  # 新增：权限拒绝异常
from django.db import models  # 新增：Q查询/聚合函数用

from .models import SalesOrder, SalesOrderItem
from products.models import Product

# 销售单列表
class SalesOrderListView(LoginRequiredMixin, ListView):
    model = SalesOrder
    template_name = 'sales/order_list.html'
    context_object_name = 'order_list'
    login_url = '/accounts/login/'

    # 只显示当前用户创建的销售单（管理员看所有）
    def get_queryset(self):
        if self.request.user.is_superuser:
            return SalesOrder.objects.all().order_by('-create_time')
        return SalesOrder.objects.filter(cashier=self.request.user).order_by('-create_time')
class SalesOrderDetailView(LoginRequiredMixin, DetailView):
    model = SalesOrder
    template_name = 'sales/order_detail.html'
    context_object_name = 'order'
    login_url = '/accounts/login/'

    # 权限控制：仅自己/管理员可查看
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser or obj.cashier == self.request.user:
            return obj
        raise PermissionDenied("无权限查看该销售单！")
# 创建销售单
class SalesOrderCreateView(LoginRequiredMixin, CreateView):
    model = SalesOrder
    template_name = 'sales/order_create.html'
    fields = []  # 表单字段手动处理
    login_url = '/accounts/login/'
    success_url = reverse_lazy('sales:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        # 传递商品列表供选择
        context['product_list'] = Product.objects.all()
        return context

    def form_valid(self, form):
        # 获取表单数据
        product_ids = self.request.POST.getlist('product_id')
        quantities = self.request.POST.getlist('quantity')

        # 校验数据
        if not product_ids or not quantities:
            form.add_error(None, '请至少选择一种商品并填写数量！')
            return self.form_invalid(form)

        # 创建销售单
        order = SalesOrder.objects.create(
            cashier=self.request.user,
            order_number=str(uuid.uuid4())[:8],
            create_time=timezone.now()
        )

        # 保存销售单明细
        for product_id, quantity in zip(product_ids, quantities):
            product = Product.objects.get(id=product_id)
            SalesOrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(quantity),
                price=product.price
            )

        return super().form_valid(form)

    def form_valid(self, form):
        # 获取表单数据
        product_ids = self.request.POST.getlist('product_id')
        quantities = self.request.POST.getlist('quantity')

        # 校验至少选择一种商品
        if not product_ids or not quantities:
            form.add_error(None, '请至少选择一种商品！')
            return self.form_invalid(form)

        # 创建销售单
        order = form.save(commit=False)
        order.cashier = self.request.user
        order.order_number = str(uuid.uuid4())[:8]
        order.create_time = timezone.now()
        order.save()

        # 保存销售单明细
        for product_id, quantity in zip(product_ids, quantities):
            product = Product.objects.get(id=product_id)
            SalesOrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        return super().form_valid(form)

    def form_valid(self, form):
        # 生成唯一销售单号
        order_code = f"SO{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # 创建销售单主表
        sales_order = form.save(commit=False)
        sales_order.order_code = order_code
        sales_order.cashier = self.request.user
        sales_order.total_amount = 0  # 初始金额为0，后续计算
        sales_order.actual_amount = 0
        sales_order.status = 1  # 已结算
        sales_order.save()

        # 处理销售单明细（从POST获取商品和数量）
        total_amount = 0
        products = self.request.POST.getlist('product_id')
        quantities = self.request.POST.getlist('quantity')

        # 检查是否有商品数据
        if not products or not quantities or len(products) != len(quantities):
            form.add_error(None, "请至少添加一种商品！")
            return self.form_invalid(form)

        for product_id, quantity in zip(products, quantities):
            if not product_id or not quantity or int(quantity) <= 0:
                continue
            
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            # 库存校验：库存不足则报错
            if product.stock_quantity < quantity:
                form.add_error(None, f"商品【{product.product_name}】库存不足！当前库存：{product.stock_quantity}")
                return self.form_invalid(form)
        
            # 扣减库存
            product.stock_quantity -= quantity
            product.save() 
            subtotal = product.sell_price * quantity
            total_amount += subtotal

            # 创建明细
            SalesOrderItem.objects.create(
                order=sales_order,
                product=product,
                sales_quantity=quantity,
                sell_price=product.sell_price,
                subtotal=subtotal
            )

        # 更新总金额
        sales_order.total_amount = total_amount
        sales_order.actual_amount = total_amount
        sales_order.save()

        return super().form_valid(form)
# Create your views here.
