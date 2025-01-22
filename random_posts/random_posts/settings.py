"""
Django settings for random_posts project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY ="django-insecure-1$#r6403zztze8g%a#m%3cyc7#f#9keq1368fk&rxp$eu5wv5s" 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "posts_app",
    "crispy_forms",
    'crispy_bootstrap5',
    "django_extensions"

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #Custom middlewares
    "posts_app.middlewares.LogRequestResponseMiddleWare.ErrorHandlingMiddleWare",
    "posts_app.middlewares.TimerMiddleWare.PerformanceMiddleware"
]

ROOT_URLCONF = "random_posts.urls"

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

WSGI_APPLICATION = "random_posts.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
DATABASES = {
    "default":{
        "ENGINE":"django.db.backends.postgresql",
        "NAME":"random_posts",
        "USER":"postgres",
        "PASSWORD":"postgres",
        "HOST":"localhost",
        "PORT":"5432"
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = 'posts_app.CustomUser'

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CRISPY_TEMPLATE_PACK = 'bootstrap5'
# LOGGING
LOG_DIR = os.path.join(BASE_DIR, "info_log")
LOG_FILE = "/api.log"
LOG_PATH = LOG_DIR + LOG_FILE

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "a") as f:
        pass # create empty log file
else:
    with open(LOG_PATH, "w") as f:  # clear log file
        f.write("")

LOGGING = {
    "version":1,
     'disable_existing_loggers': False,
     "formatters":{
         "verbose":{
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
         },
         "simple":{
              'format': '{asctime} {levelname}  {message}',
            'style': '{',
             
         }
     },
     'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'info_log','info.log'),
            'formatter': 'verbose',
        },
         'file_app': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'info_log','info_app.log'),
            'formatter': 'verbose',
        },
    },
     "loggers":{
         "django":{
             "handlers":["console","file"],
             "level":"INFO",
             "propagate":True
         },
         "posts_app":{
             "handlers":["console","file_app"],
             "level":"INFO",
             "propagate":True#set it to false if you want only the info logger to be called
         }
         
     }


}

