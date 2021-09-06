"""
Django settings for geekshop project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os, json
from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: user admin for mainapp\management\fill.db
SUPER_USER_LOGIN = env('SUPER_USER_LOGIN')
SUPER_USER_EMAIL = env('SUPER_USER_EMAIL')
SUPER_USER_PASSWORD = env('SUPER_USER_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'authapp',
    'basketapp',
    'adminapp',
    'ordersapp',
    'social_django',
    'debug_toolbar',
    'template_profiler_panel',
    'django_extensions'
]

AUTH_USER_MODEL = 'authapp.ShopUser'  # чтобы Django вместо модели User использовал в аутентификации нашу модель.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

ROOT_URLCONF = 'geekshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['geekshop/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainapp.context_processors.basket',
                'mainapp.context_processors.user_avatar',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', 'avatar']
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'authapp.pipeline.save_user_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

WSGI_APPLICATION = 'geekshop.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'  # Путь к статике из браузера

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'geekshop', 'static'),  # Путь к статике на сервере
)

# STATIC_ROOT = os.path.join(BASE_DIR, "static")
#
# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# ]
#
# DATABASES = {
#     'default': {
#         'NAME': 'geekshop-1',
#         'ENGINE': 'django.db.backends.postgresql',
#         'USER': 'postgres',
#     }
# }

if DEBUG:
    def show_toolbar(request):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'template_profiler_panel.panels.template.TemplateProfilerPanel',
    ]

MEDIA_URL = '/media/'  # Путь к изображениям из браузера

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Путь к медиа на сервере

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/auth/login/'  # for @login_required

DOMAIN_NAME = 'http://localhost:8000'

# smtp.mail.ru
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 2525
# EMAIL_HOST_USER = "name..@mail.ru"
# EMAIL_HOST_PASSWORD = "pass.."
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# SERVER_EMAIL = EMAIL_HOST_USER
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# https://mailtrap.io/
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = '2525'
EMAIL_USE_SSL = False
EMAIL_USE_TLS = False

# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = None, None

# Вариант python -m smtpd -n -c DebuggingServer localhost:25
# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = None, None

# Вариант логирования сообщений почты в виде файлов вместо отправки
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = 'tmp/email-messages/'

# Константа с кортежем бэкендов аутентификации
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.odnoklassniki.OdnoklassnikiOAuth2',
)

# # Загружаем секреты из файла
# with open('geekshop/vk.json', 'r') as f:
#     VK = json.load(f)

# SOCIAL_AUTH_VK_OAUTH2_KEY = VK['SOCIAL_AUTH_VK_OAUTH2_KEY']
# SOCIAL_AUTH_VK_OAUTH2_SECRET = VK['SOCIAL_AUTH_VK_OAUTH2_SECRET']

# Загружаем секреты из виртуального окружения
SOCIAL_AUTH_VK_OAUTH2_KEY = env('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = env('SOCIAL_AUTH_VK_OAUTH2_SECRET')

SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = env('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY')  # Application ID
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = env('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET')  # Секретный ключ приложения
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = env('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME')  # Публичный ключ
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_ACCESS_TOKEN = env('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_ACCESS_TOKEN')
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SESSION_SECRET_KEY = env('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SESSION_SECRET_KEY')
SOCIAL_AUTH_URL_NAMESPACE = 'social'
