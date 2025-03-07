# -*- coding: UTF-8 -*-
# @创建时间: 2024/12/12 10:34   -- yh 
# @文件名:      dev_settings.py

# 开发环境设置
"""
Django settings for meiduo project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import datetime
from pathlib import Path
from . import my_git_ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1snf_w0s!&+%rp$p8uw!j#fh&xpqfs@tidu^_d%qgnua+bqm$j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "apps.users.apps.UsersConfig",
    'apps.content.apps.ContentConfig',
    'apps.verifications.apps.VerificationsConfig',
    'apps.areas.apps.AreasConfig',
    'apps.goods.apps.GoodsConfig',
    'apps.carts.apps.CartsConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.meiduo_admin.apps.MeiduoAdminConfig',
    'corsheaders',


]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.jinja2.Jinja2',  # jinja2模板引擎
        'DIRS'    : [BASE_DIR.parent / 'templates'],
        'APP_DIRS': True,
        'OPTIONS' : {
            # 补充Jinja2模板引擎环境
            'environment'       : 'meiduo.utils.jinja2_env.jinja2_environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {  # 原来的django模板引擎
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [BASE_DIR.parent / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS' : {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql',
        'HOST'    : '127.0.0.1',
        'port'    : 3306,
        'USER'    : my_git_ignore.MYSQL_USER,
        'PASSWORD': my_git_ignore.MYSQL_PASSWORD,
        'NAME'    : 'meiduo'
    }
}
# 缓存配置
CACHES = {
    "default"    : {  # 默认 缓存后端- default
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS" : {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session"    : {  # session 缓存后端- session
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS" : {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {  # verify_code 缓存后端- 验证码相关
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS" : {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history"    : {  # history 缓存后端- 浏览商品历史
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS" : {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts"      : {  # carts 缓存后端- 购物车相关
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS" : {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# 表示会话数据将存储在缓存中
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 指定了使用哪个缓存后端来存储会话数据
SESSION_CACHE_ALIAS = "session"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

# 设置中文
LANGUAGE_CODE = 'zh-Hans'
# 亚洲上海时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# 指定加载静态文件的路由前缀
STATIC_URL = '/static/'

# 配置静态文件加载路径
STATICFILES_DIRS = [BASE_DIR.parent / 'static', ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 配置日志文件
LOGGING = {
    'version'                 : 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters'              : {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple' : {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters'                 : {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers'                : {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level'    : 'INFO',
            'filters'  : ['require_debug_true'],
            'class'    : 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file'   : {  # 向文件中输出日志
            'level'      : 'INFO',
            'class'      : 'logging.handlers.RotatingFileHandler',
            'filename'   : BASE_DIR / 'logs/meiduo.log',  # 日志文件的位置
            'maxBytes'   : 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter'  : 'verbose'
        },
    },
    'loggers'                 : {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers' : ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level'    : 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# 自定义的用户模型类
AUTH_USER_MODEL = 'users.User'
# 指定自定义的用户认证后端
AUTHENTICATION_BACKENDS = [
    # 'apps.users.utils.UsernameMobileAuthBackend',
    'meiduo.utils.authenticate.MeiduoModelBackend'
]

LOGIN_URL = '/login/'

# 邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
EMAIL_HOST = 'smtp.yeah.net'  # 发邮件主机
EMAIL_PORT = 25  # 发邮件端口
EMAIL_HOST_USER = 'meiduo_postemail@yeah.net'  # 授权的邮箱

EMAIL_HOST_PASSWORD = my_git_ignore.EMAIL_HOST_PASSWORD  # 邮箱授权时获得的密码，非注册登录密码

EMAIL_FROM = '美多商城<meiduo_postemail@yeah.net>'  # 发件人抬头

# 邮箱验证链接
EMAIL_VERIFY_URL = 'http://127.0.0.1:8000/emails/verification/'

# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = 'meiduo.utils.fastdfs.fdfs_storage.FastDFSStorage'

# FastDFS相关参数
FDFS_BASE_URL = 'http://23.95.240.187:8888/'

# CORS  跨域
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
)
CORS_ALLOW_CREDENTIALS = True

# JWT
REST_FRAMEWORK = {
    # 只能固定认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 替换为新类
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),

}  # dev_settings.py 中的 SIMPLE_JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME'       : datetime.timedelta(days=1),
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),  # ✅ 允许 JWT 格式
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.meiduo_admin.utils.jwt_response_payload_handler',  # 关键配置
}

# # 新增 JWT 配置（可选）
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME'       : datetime.timedelta(days=1),
#     # 'ROTATE_REFRESH_TOKENS'       : True,
#     # 新增以下一行：指定自定义的payload处理函数
#     'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.meiduo_admin.utils.jwt_response_payload_handler',
# }
