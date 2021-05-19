#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: lxw
@license: ZJU Licence
@contact: 2096497236@qq.com
@site: https://www.lylinux.net/
@software: VSCode
@file: urls.py
@time: 2018/2/25 下午3:04
"""
from django.urls import path
from . import views

app_name = "law_stat"

urlpatterns = [
    path('law_stat/init_law_data',views.make_law_init,name = 'init_law_data'),
    path('law_stat/view_law_provision',views.view_law_provision,name = 'view_law_provision'),
    path('law_stat/test_view',views.test_view,name = 'view_law_provision'),
    path('law_stat/get_law_provision',views.get_law_provision,name = 'get_law_provision'),
    path('law_stat/test_post',views.test_post,name = 'test_postw'),
    path('law_stat/test_word_cloud',views.test_word_cloud,name = 'test_postw'),
    
    
]
