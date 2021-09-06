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
        
admin.site.register(Profile),
admin.site.register(Upload_csv),
admin.site.register(Resultat),
admin.site.register(Critere),
admin.site.register(Subcritere),
