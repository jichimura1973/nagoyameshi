"""
Django settings for nagoyameshi project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vuqt5t8+n7q530-#7)^l7b=z4z54r8k^#5ozd!##yfe+mzz&l7"

# SECURITY WARNING: don't run with debug turned on in production!
if os.path.exists('./.is_debug'):
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com', '*']
# ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # my apps
    "restaurant",
    "accounts",
    # allauth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "storages",
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'django.middleware.locale.LocaleMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    # 追加
    INTERNAL_IPS = ['127.0.0.1']
    # 追加
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : lambda request: True,
    }

ROOT_URLCONF = "nagoyameshi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nagoyameshi.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = 'ja'

# https://docs.djangoproject.com/en/4.2/topics/i18n/

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
)

# メディアファイルの設定
# MEDIA_URL = "media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# DJANGO_SETTINGS_MODULE = "allauth.account.forms"

# staticファイルの参照先
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# # mediaファイル保存先
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# # アクセスキーID
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
# # シークレットアクセスキー
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
# # バケット名
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
# 保存先URL
# STATIC_URL = "static/"

STATIC_URL = 'https://%s.s3.ap-northeast-1.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
AWS_LOCATION = 'static'


# allauth
AUTH_USER_MODEL = "accounts.CustomUser"

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend", # 一般ユーザー用（メール認証）
    "django.contrib.auth.backends.ModelBackend", # 管理サイト用（ユーザー名認証）
)

# メールアドレス認証に変更する設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True

# サインアップにメールアドレス確認を行わない設定
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'top_page'
ACCOUNT_LOGOUT_REDIRECT_URL = 'top_page'

# ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET = True

# allauth アダプタ
ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

# ログインフォームのカスタム用設定
ACCOUNT_FORMS = {
'login': 'accounts.forms.MyLoginForm',
'signup': 'accounts.forms.MySignupForm',
}

# if DEBUG == False:
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# メールサーバーの設定
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = True
