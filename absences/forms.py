#-*- coding: utf-8 -*-
from django import forms
from absences.models import Etudiant, Matiere

class ConnexionForm(forms.Form):
	identifiant = forms.CharField(label='Identifiant', max_length=30)
	motDePasse = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

class JustificatifForm(forms.Form):
	raison = forms.CharField(label='Raison', max_length = 100)
	# dateDebut = forms.DateField(label='Date début effet')
	# dateFin = forms.DateField(label='Date fin effet')
	# matiere = forms.CharField(label='Matière', max_length=30)

class JustificatifMultipleForm(forms.Form):
	etudiant = forms.ChoiceField(choices=[(e.user.id, e.user.last_name + ' ' + e.user.first_name) for e in Etudiant.objects.all().order_by('user__last_name')])
	matieres = forms.MultipleChoiceField(choices=[(m.id, m.intitule) for m in Matiere.objects.all().order_by('intitule')])
	dateDebut = forms.DateTimeField(label='Date début effet')
	dateFin = forms.DateTimeField(label='Date fin effet')
	raison = forms.CharField(label="Raison", max_length=100)