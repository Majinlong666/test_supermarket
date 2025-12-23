from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # 销售单列表
    path('list/', views.SalesOrderListView.as_view(), name='order_list'),
    # 创建销售单
    path('create/', views.SalesOrderCreateView.as_view(), name='order_create'),
    path('detail/<int:pk>/', views.SalesOrderDetailView.as_view(), name='order_detail'),
]
