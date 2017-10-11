"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from blog.views import SignUp

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),  # Anything but /admin/
    url(r'^account/signup/$', SignUp.as_view(), name='signup'),
    url(r'^account/login/$', views.login, name='login'),
    url(r'^account/logout/$', views.logout, name='logout', kwargs={'next_page':'/'}),
]
