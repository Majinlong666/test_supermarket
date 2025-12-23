# /supermarket/accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db import models
from django.db.models import Sum

class LoginView(View):
    """登录视图"""
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            # 检查是否在职
            if hasattr(user, 'employee') and not user.employee.status:
                messages.error(request, '该账号已离职，无法登录！')
                return render(request, self.template_name)
            # 登录
            login(request, user)
            messages.success(request, f'欢迎回来：{user.get_full_name() or user.username}')
            return redirect('dashboard')
        else:
            messages.error(request, '账号/密码错误！')
            return render(request, self.template_name)

# 仪表盘（首页）
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib import messages

class LogoutView(DjangoLogoutView):
    """注销视图"""
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, '您已成功注销！')
        return super().dispatch(request, *args, **kwargs)

# Create your views here.
