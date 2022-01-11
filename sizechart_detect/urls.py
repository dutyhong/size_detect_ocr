# 作者 ：duty
# 创建时间 ：2022/1/7 4:17 下午
# 文件 ：urls.py
from django.conf.urls import url

from sizechart_detect import views

urlpatterns = [
    url(r'^', views.add),
]