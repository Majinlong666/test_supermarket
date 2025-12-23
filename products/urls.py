from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # 商品列表
    path('list/', views.ProductListView.as_view(), name='product_list'),
    # 添加商品
    path('add/', views.ProductCreateView.as_view(), name='product_add'),
     path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),  # 新增
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),  # 新增
    # 搜索商品
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
]
