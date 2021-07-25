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
    # vaccin.html/
    path('vaccins', views.vccins_page, name='vaccins_page'),
    # data_page.html/
    path('data_page', views.ahp_page, name='data_page'),
    # home.html
    path('', views.home_view, name='home'),
    # API page
    path('api', views.api, name='api'),
    path('api2', views.api2, name='api2'),
    # test_ahp/
    # path('test_ahp/', views.create_critere_model_form, name = 'test_ahp'),
    path('create_normal/', views.create_critere_normal, name = 'create_critere_normal'),
    path('list/', views.CritereListView.as_view(), name = 'critere_list'),
    path('create_with_subcritere/', views.create_critere_with_subcritere,
     name = 'create_critere_with_subcritere'),
    path('teser_tableau_ta3k/', views.test_csv_ahp, name = 'teser_tableau_ta3k'),
    path('aimen/', views.aimen_methode, name = 'aimen_methode'),
    path('haka/', views.save_critere_as_csv, name = 'haka'),
    path('result/',views.show_resultat, name = "result"),

    path('chkla/',views.tester_chkla_ta3i, name = "chkla"),
    path('chart4/', views.chart_for, name = "chart_four"),
    path('promthee2/', views.promether_view, name = "promethee_2"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
