#-*- coding: utf-8 -*-
from django import forms

class ConnexionForm(forms.Form):
	identifiant = forms.CharField(label='Identifiant', max_length=30)
	motDePasse = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)