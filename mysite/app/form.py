from django import forms
from django.forms import fields
from django.forms.models import modelformset_factory
from .models import *
from django.forms import formset_factory
from .models import Critere, Subcritere


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(initial='Your first name')
    last_name = forms.CharField(initial='Your last name')
    city = forms.CharField(initial='Your city')
    country = forms.CharField(initial='Your country')
    adress = forms.CharField(initial='Your adress')
    phone_number = forms.CharField(initial='Your phone number')
    class Meta:
        model = Profile
        exclude = ['user']
        

# class Effets_secondairesForm(forms.ModelForm):
#     class  Meta:
#        model = Effets_secondaires
#        fields = '__all__'   

# class VaccinsForm(forms.ModelForm):
#     class  Meta:
#        model = Vaccins
#        fields = ['nom_vaccin',]

# class CoutForm(forms.ModelForm):
#     class  Meta:
#        model = Cout
#        fields = '__all__' 

# class PosologieForm(forms.ModelForm):
#     class  Meta:
#        model = Posologie
#        fields = '__all__' 

# class CharacteristiquesForm(forms.ModelForm):
#     class  Meta:
#        model = Characteristiques
#        fields = '__all__'        
# Models Form 
# here i want to creat autoatique forms
#  start agin Sun, 11 ,21

class CritereForm(forms.Form):
    name = forms.CharField(
        label='Critere Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Critere Name here'
        })
    )
# CritereFormset = formset_factory(CritereForm, extra=5)    

# class CritereModelForm(forms.ModelForm):

#     class Meta:
#         model = Critere
#         fields = '__all__'
#         labels = {
#             'name': 'Critere Name'
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Critere Name here'
#                 }
#             )
#         }
# CritereFormset = formset_factory(CritereForm) 
# CHOICE = Critere.objects.all()
# CritereModelFormset = modelformset_factory(
#     Critere,
#     fields=('name', ),
#     # fields=('name',),
#     extra=5,
#     widgets={
#         'name': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter Critere Name here'
#             }
#         )
#     }
# )   
# SubcritereFormset = modelformset_factory(
#     Subcritere,
#     fields=('name', ),
#     extra=1,
#     widgets={'name': forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter Subcritere Name here'
#         })
#     }
# )


AlternativeModelFormset = modelformset_factory(
    Alternative,
    fields=('nom_vaccin', ),
    extra=5,
    widgets={'nom_vaccin': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Vaccin Name here'
        })
    }
)
CritereModelFormset = modelformset_factory(
    Critere,
    fields=('name', ),
    extra=5,
    widgets={'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Critere Name here'
        })
    }
)

class CritereCritere(forms.ModelForm):
    name = forms.CharField(        
    )       
    class Meta:
        model = Critere
        exclude = ('user',)     

        