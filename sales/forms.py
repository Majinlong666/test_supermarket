# /supermarket/sales/forms.py
from django import forms
from django.forms import formset_factory
from products.models import Product

class SalesOrderItemForm(forms.Form):
    """销售单商品项表单"""
    product_id = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control product-select'}),
        label='商品',
        required=False
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control quantity', 'min': '1'}),
        label='数量',
        min_value=1,
        required=False
    )

    def clean(self):
        """验证商品和数量"""
        cleaned_data = super().clean()
        product_id = cleaned_data.get('product_id')
        quantity = cleaned_data.get('quantity')

        if not product_id or not quantity:
            raise forms.ValidationError('请选择商品并填写数量')
        return cleaned_data

# 动态生成多商品表单集
SalesOrderFormSet = formset_factory(SalesOrderItemForm, extra=1)
