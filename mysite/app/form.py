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

class CritereForm(forms.Form):
    name = forms.CharField(
        label='Critere Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Critere Name here'
        })
    )

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



        


        