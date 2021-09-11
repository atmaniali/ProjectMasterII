from django import forms
from django.forms import formset_factory

class AlternativeForm(forms.Form):
    nom_vaccin = forms.CharField(
        label='Nom de Vaccin',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Vaccin Name here'
        })
    )
AlternativeFormset = formset_factory(AlternativeForm, extra=1)    