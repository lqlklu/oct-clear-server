"""oct_denoise_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from oct_denoise.views import upload_images, image, fetch_all, sign_up, sign_in

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_images/', upload_images),
    path('image/<path:p>', image),
    path('fetch_all/<int:uid>', fetch_all),
    path('signup/', sign_up),
    path('signin/', sign_in),
]
