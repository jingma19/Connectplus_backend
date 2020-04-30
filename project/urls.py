"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from ConnectPlus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_fb', views.login_fb_action, name='login_fb'),
    path('add_task', views.add_task_action, name='add_task'),
    path('get_username_from_token', views.get_username_from_token, name='get_username_from_token'),
    path('get_task', views.task_action, name='get_task'),
    path('complete_task', views.complete_task_action, name='complete_task'),
    path('get_health', views.health_action, name='get_health'),
    path('add_health', views.add_health_action, name='add_health'),
    path('get_news', views.news_action, name='get_news'),
    path('erase_data', views.erase_data_action, name='erase_data'),
    path('add_partner', views.add_partner_action, name='add_partner'),
]
