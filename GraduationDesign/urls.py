"""GraduationDesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from django.views.generic import RedirectView

from users import views
from backgroundData import index
from backgroundData import addData
from backgroundData import queryData

urlpatterns = [
    path('favicon.ico',RedirectView.as_view(url=r'static/img/favicon.ico')),
    path('admin/', admin.site.urls),
    path('',index.commodity_id, name="index"),
    path('add/',addData.commodity_id1, name="add"),
    path('query/',queryData.select_id, name="query"),


    path('users/',include('users.urls')),
    path('users/',include('django.contrib.auth.urls')),

]
