import os
import pymysql

# 解决Django识别pymysql的问题（核心！）
pymysql.install_as_MySQLdb()

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 安全密钥（开发环境用，生产环境替换为随机字符串）
SECRET_KEY = 'django-insecure-abc1234567890!@#$%^&*()_+-=[]{}|;:,.<>?'

# 开发环境调试模式
DEBUG = True
ALLOWED_HOSTS = ['*']  # 允许所有IP访问

# 应用注册（核心！直接写应用名，无层级）
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方插件
    'django_bootstrap5',
    'axes',
    # 自定义应用（直接放在根目录）
    'accounts',
    'sales',
    'products',
    'suppliers',
]

# 中间件（默认，无需修改）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

# 根路由配置
ROOT_URLCONF = 'supermarket.urls'

# 模板配置（核心：指定templates目录）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [r"C:\Users\86157\Music\supermarket\supermarket\templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'supermarket.wsgi.application'

# 数据库配置（关键！替换为你的MySQL密码）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'supermarket_management',  # 数据库名（后续创建）
        'USER': 'root',                     # MySQL用户名
        'PASSWORD': 'root',                 # 替换为实际密码！
        'HOST': '10.15.130.209',                # 本地数据库
        'PORT': '3306',                     # 默认端口
        'OPTIONS': {
            'charset': 'utf8mb4'            # 支持中文
        }
    }
}

# 密码验证（默认）
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 语言+时区（中文+上海）
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # 静态文件目录
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    # 生产环境收集用

# 默认主键
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 登录配置
LOGIN_URL = '/accounts/login/'          # 未登录跳转页
LOGIN_REDIRECT_URL = '/dashboard/'      # 登录后跳转页
LOGOUT_REDIRECT_URL = '/accounts/login/'# 退出后跳转页
