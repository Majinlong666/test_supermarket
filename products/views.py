from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product
from suppliers.models import Supplier
from django.contrib import messages
from django.db.models import Q

# 商品列表
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'product_list'
    login_url = '/accounts/login/'
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_edit.html'
    fields = ['product_code', 'product_name', 'category', 'supplier', 'purchase_price', 'sell_price', 'stock_quantity', 'warning_quantity']
    login_url = '/accounts/login/'
    success_url = reverse_lazy('products:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context['supplier_list'] = Supplier.objects.all()
        context['title'] = '编辑商品'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"商品【{form.instance.product_name}】编辑成功！")
        return super().form_valid(form)

# 删除商品
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    login_url = '/accounts/login/'
    success_url = reverse_lazy('products:product_list')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f"商品【{product.product_name}】删除成功！")
        return super().delete(request, *args, **kwargs)
# 添加商品
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_add.html'
    fields = ['product_code', 'product_name', 'category', 'supplier', 'purchase_price', 'sell_price', 'stock_quantity', 'warning_quantity']
    login_url = '/accounts/login/'
    success_url = reverse_lazy('products:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        # 传递供应商列表
        context['supplier_list'] = Supplier.objects.all()
        return context
# Create your views here.

# 商品搜索
class ProductSearchView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'product_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(product_name__icontains=query) | Q(product_code__icontains=query)
            )
        return Product.objects.all()