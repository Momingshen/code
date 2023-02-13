"""fileload URL Configuration

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
from django.urls import path, re_path as url, include
from app.views import user, upload, download, power, config
from django.views import static  ##新增
from django.conf import settings  ##新增

urlpatterns = [
    path("power/", power.PowerViews.as_view()),

    # path("power/add/", power.power_add),
    # path("power/edit/", power.power_edit),
    # path("power/save/", power.power_save),
    # path("power/get/", power.power_get),
    path("login/", user.login_index, name="login"),
    url("^$", user.login_index),
    path("logout/", user.loginout),
    path("admin/", admin.site.urls),
    path("config/", config.ConfigViews.as_view()),
    path("user/empower/", user.user_empower),
    path("user/nopower/", user.user_nopower),
    path("user/power/", user.user_power),
    path("user/list/", user.user_list),
    path("user/del/", user.user_del),
    path("user/pw/", user.user_pw),
    path("user/resetPw/", user.reset_pw),
    path("upload/list/", upload.upload_list),
    path("people/list/", user.people_list),
    path("download/list/", download.download_list),
    path("download/mysql/", download.download_mysql),
    path("top/", user.top),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
