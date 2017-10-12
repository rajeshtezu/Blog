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
from django.contrib.auth.views import ( login, logout, password_reset, password_reset_done,
                                        password_reset_confirm, password_reset_complete )
from django.contrib.auth.views import PasswordResetView

from blog.views import SignUp

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),  # Anything but /admin/
    url(r'^account/signup/$', SignUp.as_view(), name='signup'),
    url(r'^account/login/$', login, name='login'),
    url(r'^account/logout/$', logout, name='logout', kwargs={'next_page':'/'}),
    url(r'^account/reset-password/$', password_reset, name='reset_password'),
    url(r'^account/reset-password/done/$', password_reset_done, name='password_reset_done'),
    url(r'^account/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^account/reset-password/complete/$', password_reset_complete, name='password_reset_complete'),
]
