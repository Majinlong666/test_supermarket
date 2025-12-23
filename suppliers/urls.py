from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    # 供应商列表
    path('list/', views.SupplierListView.as_view(), name='supplier_list'),
    # 添加供应商
    path('add/', views.SupplierCreateView.as_view(), name='supplier_add'),
]
