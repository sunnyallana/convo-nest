"""
URL configuration for ConvoNest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls'))
]

# This line is used to add a URL pattern for serving media files in development.
# settings.MEDIA_URL is the URL that will be used to access the media files.
# document_root=settings.MEDIA_ROOT specifies the directory where the media files are stored.
# Note: This is not suitable for production use! For production, use a web server or a service like AWS S3 to serve static files.

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
