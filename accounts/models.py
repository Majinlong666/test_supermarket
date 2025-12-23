# /supermarket/accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    """员工信息扩展表（关联Django内置User）"""
    ROLE_CHOICES = [
        ('user', '普通用户'),
        ('admin', '管理员'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee', verbose_name='关联用户')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    status = models.BooleanField(default=True, verbose_name='是否在职')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='角色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '员工信息'
        verbose_name_plural = '员工信息'

    def __str__(self):
        return self.user.get_full_name() or self.user.username
