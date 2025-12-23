from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Supplier

# 供应商列表
class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'supplier_list'
    login_url = '/accounts/login/'

# 添加供应商
class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    template_name = 'suppliers/supplier_add.html'
    fields = ['supplier_name', 'contact_person', 'phone', 'address']
    login_url = '/accounts/login/'
    success_url = reverse_lazy('suppliers:supplier_list')
# Create your views here.
