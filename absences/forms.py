#-*- coding: utf-8 -*-
from django import forms

class ConnexionForm(forms.Form):
	identifiant = forms.CharField(label='Identifiant', max_length=30)
	motDePasse = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

class JustificatifForm(forms.Form):
	raison = forms.CharField(label='Raison', max_length = 100)
	# dateDebut = forms.DateField(label='Date début effet')
	# dateFin = forms.DateField(label='Date fin effet')
	# matiere = forms.CharField(label='Matière', max_length=30)

class JustificatifMultipleForm(forms.Form):
	# etudiant = forms.Select(label="Etudiant")
	# matieres = forms.SelectMultiple(label="Matières")
	dateDebut = forms.DateField(label='Date début effet')
	dateFin = forms.DateField(label='Date fin effet')
	raison = forms.CharField(label="Raison", max_length=100)