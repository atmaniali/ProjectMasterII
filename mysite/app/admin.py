# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *
# Register your models here.
class AdminUser(admin.ModelAdmin):
    class Meta:
        model = Profile
class CritereAdmin(admin.ModelAdmin):
    list_display = ['name','created_at',]  
    search_fields = ['name','created_at',]   
class SubcritereAdmin(admin.ModelAdmin):
    list_display = ['name','created_at','critere']  
    search_fields = ['name','created_at','critere__name'] 

        
admin.site.register(Profile),
admin.site.register(Upload_csv),
admin.site.register(Resultat),
admin.site.register(Critere, CritereAdmin),
admin.site.register(Subcritere, SubcritereAdmin),
admin.site.register(Alternative),
admin.site.register(AHP_file),
