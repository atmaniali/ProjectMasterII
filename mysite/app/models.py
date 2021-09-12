# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile' ,null = True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank= True, null=  True)
    last_name = models.CharField(max_length=200, blank= True, null=  True)
    city = models.CharField(max_length=200, blank= True, null=  True)
    country = models.CharField(max_length=200, blank= True, null=  True)
    adress = models.CharField(max_length=200, blank= True, null=  True)
    phone_number = models.CharField(max_length=200, blank= True, null=  True)
    
    

    def __str__(self):
        return self.user.username
    

    @receiver(post_save, sender=User) #add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User) #add this
    # instancewin you want to create a model to profile
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    # file = models.FileField(upload_to = 'files', blank=True, null= True)
    # TODO: add adress later (don't forget to makemigrations and migrate)
   

# Class for groupe of creteria

class Upload_csv(models.Model):
    user = models.ForeignKey(Profile, related_name= 'upload_csv', on_delete= models.CASCADE)
    file_csv = models.FileField(upload_to='media/files/', null= True, default='default.csv')
    def __str__(self):
        return self.file_csv
    


class Resultat(models.Model):
    key = models.CharField(max_length=100)
    value = models.FloatField()
    def __str__(self):
            return self.key

# critere table
# critere table
class Critere(models.Model):
    name = models.CharField(max_length=200, null=  True, unique = True)
    created_at = models.DateTimeField(auto_now_add=True, null=  True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'critere'
        ordering = ['-created_at']
        

    def __str__(self):
        return self.name

    def get_subcriters(self):
        return ', '.join(self.subcriters.all().values_list('name', flat=True)) 
    def get_pk(self):
        return self.pk  
    def get_name(self):
        return self.name         
    
        
class Subcritere(models.Model):

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=  True)
    critere = models.ForeignKey(
        Critere,
        related_name='subcriters', on_delete=models.SET_NULL,
        null=True)

    class Meta:
        db_table = 'subcritere'

    def __str__(self):
        return self.name
    def get_pk(self):
        return self.pk     
        
class Alternative(models.Model):
    nom_vaccin = models.CharField(max_length=200)
    def __str__(self) :
        return self.nom_vaccin
    def get_name(self):
          return self.nom_vaccin  
    def get_pk(self):
        return self.pk      

class Save_result(models.Model):
    name= models.CharField(max_length=200)
    dictionnaire = models.JSONField()

    def __str__(self):
        return self.name

class Taille(models.Model):
    rows = models.IntegerField() 
    colmn =   models.IntegerField()   
    def __str__(self) :
        return str(self.rows )
    def get_pk(self):
        return self.pk    

# class weights(models.Model):
#     weight = models.CharField(max_length = 200)
#     value  = models.IntegerField()

    
        
