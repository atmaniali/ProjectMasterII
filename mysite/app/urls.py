# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

app_names='app'


urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    # /Profile.html
    path('profile', views.profile, name='profile'),
    # vaccin.html/
    path('vaccins', views.vccins_page, name='vaccins_page'),
    # data_page.html/
    path('data_page', views.ahp_page, name='data_page'),
    # home.html
    path('home', views.home_view, name='home'),
    # API page
    path('api', views.api, name='api'),
    path('api2', views.api2, name='api2'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
