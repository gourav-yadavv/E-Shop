"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%($m3w=*5yp)6_%@y_6ulv2!!)h9ca!2-fn+lmldkzm&b%(lzo'

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
    'store.apps.StoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# This is the URL where media files will be served from.
MEDIA_URL = '/images/'


# This is the local file system path where media files will be stored.
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

# for above two lines of code
# Certainly! The code you provided is related to configuring media files in a Django project's settings.py file. Media files are typically user-uploaded files like images, videos, documents, etc. The configuration you've posted helps Django handle these media files properly. Here's a detailed explanation for each part:

# MEDIA_URL: This is a URL prefix that will be used to serve media files. When a user requests a media file (like an image), Django will use this URL prefix to locate and serve the file. In this case, any media files will be served from URLs starting with /images/.

# MEDIA_ROOT: This is the absolute file system path where media files will be stored on the server. The os.path.join(BASE_DIR, 'static/images') part constructs a path by joining the base directory of your Django project (BASE_DIR) with the directory static/images. So, on the server, your media files will be stored in the static/images directory.

# To explain further:

# Media URL (MEDIA_URL): This is like a web address where users can access their uploaded files. When a user uploads an image, for instance, it's stored on the server in a specific folder (MEDIA_ROOT). This URL is how the user's browser requests the image when it's displayed on a webpage. So, if you have an image called my_image.jpg, its URL would be something like /images/my_image.jpg.

# Media Root (MEDIA_ROOT): This is the physical location on your server's file system where uploaded media files are stored. It's the place where Django saves and retrieves media files. For example, when a user uploads an image through your website, Django will save that image in the MEDIA_ROOT directory.

# Remember that when you're working in development mode, Django's built-in development server handles serving static and media files for you. In a production environment, you'll need to configure your web server (like Apache or Nginx) to serve these files.

# These settings help your Django project manage user-uploaded media files in a structured and accessible way, making it easier to display and manage content like images in your web application.

