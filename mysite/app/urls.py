# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

app_names='app'


urlpatterns = [

    # The home page
    path('index/', views.index, name='index'),
    # /Profile.html
    path('profile', views.profile, name='profile'),
    # home.html
    path('', views.home_view, name='home'),
    path('create_normal/', views.create_critere_normal, name = 'create_critere_normal'),
    path('list/', views.CritereListView.as_view(), name = 'critere_list'),
    path('create_with_subcritere/', views.create_critere_with_subcritere,
     name = 'create_critere_with_subcritere'),
    path('promthee2/', views.promether_view, name = "promethee_2"),
    path('ahp/', views.ahp_final, name = "ahp"),
    path('maps/', views.maps, name = 'maps'),
    #methode I
    path('creating/', views.creating, name ='creating'),
    path('show/', views.shows, name = 'show'),
    path('listes/', views.listes, name = 'listes'),
    #methode II
    path('creating_sub/', views.creating_sub, name ='creating_sub'),
    path('show_sub/', views.show_sub, name = 'show_sub'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
