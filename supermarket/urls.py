from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from accounts.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 仪表盘
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # 账号管理
    path('accounts/', include('accounts.urls')),
    # 销售管理
    path('sales/', include('sales.urls')),
    # 商品管理
    path('products/', include('products.urls')),
    # 供应商管理
    path('suppliers/', include('suppliers.urls')),
    # 退出登录
    path('logout/', LogoutView.as_view(), name='logout'),
    # 根路径重定向
    path('', lambda req: redirect('dashboard')),
]
