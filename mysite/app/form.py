from django import forms
from django.forms import fields
from django.forms.models import modelformset_factory
from .models import *
from django.forms import formset_factory
from .models import Critere, Subcritere


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

class CritereModelForm(forms.ModelForm):

    class Meta:
        model = Critere
        fields = '__all__'
        labels = {
            'name': 'Critere Name'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Critere Name here'
                }
            )
        }
CritereFormset = formset_factory(CritereForm) 
CritereModelFormset = modelformset_factory(
    Critere,
    fields=('name','user' ),
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Critere Name here'
            }
        )
    }
)   
SubcritereFormset = modelformset_factory(
    Subcritere,
    fields=('name', ),
    extra=1,
    widgets={'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Subcritere Name here'
        })
    }
)

