"""zhihuimohe4py URL Configuration

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
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import include, path
from base.appview import index_views
from base import websocket_terminal
from zhkt import websocket_ytj, websocket_stu


urlpatterns = [
    path(r'favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),  # favicon位置
    path('', index_views.to_index),  # 首页
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # 基础信息
    path('', include('sr.urls')),  # 盒子和设备相关硬件管理
    path('zhkt/', include('zhkt.urls')),  # 智慧课堂模块
    path('', include('apiweb.urls')),  # 开放的api接口
    # 所有webSocket
    path(r'ecc/ws', websocket_terminal.ws_hp_in),  # 画屏接入智慧魔盒
    path(r'zhktYtj/ws', websocket_ytj.ws_ytj_in),  # 一体机连入智慧魔盒
    path(r'wxs/zhkt4StuWs', websocket_stu.ws_ytj_stu_in),  # 学生端接入智慧魔盒
]
