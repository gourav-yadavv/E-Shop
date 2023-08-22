"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

# Certainly! The below line of code is related to configuring URL patterns for serving media files in a Django project. 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns: This is a list of URL patterns that Django uses to route incoming requests to specific views or functionalities in your web application. It determines how different URLs are handled and what content is displayed on those URLs.

# +=: This is a Python operator that concatenates (adds together) two lists. In this case, it's used to add a new URL pattern to the existing list of URL patterns.

# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT): This function call adds a URL pattern for serving media files. It tells Django how to handle requests for media files and where to find them on the server.

# static: This is a built-in Django function that generates a URL pattern for serving static files (like media files).

# settings.MEDIA_URL: This is the URL prefix that you defined in your project's settings.py file using the MEDIA_URL setting. It specifies the URL where media files will be served from. For example, if MEDIA_URL is /images/, this URL pattern will match requests starting with /images/.

# document_root=settings.MEDIA_ROOT: This is the absolute file system path where media files are stored on the server, as defined in your project's settings.py using the MEDIA_ROOT setting. This tells Django where to look for the requested media files on the server's file system.

# So, when a user's browser requests a media file (like an image) using a URL that matches the MEDIA_URL prefix, Django's static function will use the provided document_root to locate the file on the server and serve it to the user's browser.

# In simple terms, this line of code sets up a URL pattern that allows your Django project to serve user-uploaded media files (like images) when they are requested by a user's  browser. It's like telling Django how to show the images and other files that users upload to your website. So, when someone wants to see a picture they uploaded, this line makes sure that Django knows where to find the picture and show it on the webpage.