from django import forms
from django.forms import fields
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class Effets_secondairesForm(forms.ModelForm):
    class  Meta:
       model = Effets_secondaires
       fields = '__all__'   

class VaccinsForm(forms.ModelForm):
    class  Meta:
       model = Vaccins
       fields = ['nom_vaccin',]

class CoutForm(forms.ModelForm):
    class  Meta:
       model = Cout
       fields = '__all__' 

class PosologieForm(forms.ModelForm):
    class  Meta:
       model = Posologie
       fields = '__all__' 

class CharacteristiquesForm(forms.ModelForm):
    class  Meta:
       model = Characteristiques
       fields = '__all__'        