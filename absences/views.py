#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout	
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.template import RequestContext

from absences.models import Cours, Absence, Justificatif, Etudiant
from absences.forms import ConnexionForm, JustificatifForm, JustificatifMultipleForm

from datetime import datetime
from calendar import monthrange


#DEBUG 


import pdb


def index(request):
	return render(request, 'absences/index.html')

# Permet la connexion
def connexion(request):
	error = False
	if request.method == 'POST':
		form = ConnexionForm(request.POST)

		if form.is_valid():
			identifiant = form.cleaned_data['identifiant']
			motDePasse = form.cleaned_data['motDePasse']
			user = authenticate(username=identifiant, password=motDePasse)
			if user:
				login(request, user)
				messages.success(request, 'Vous êtes bien connecté !')
				return redirect(reverse('absences:index'))
			else:
				error = True
	else:
		form = ConnexionForm()
	return render(request, 'absences/connexion.html', {'form':form})

# Permet la déconnexion
def deconnexion(request):
	logout(request)
	return redirect(reverse('absences:index'))

# Affiche tous les cours de la bdd
class CoursListView(ListView):
	model = Cours
	context_object_name = 'listeCours'
	template_name = 'absences/listeCours.html'
	paginate_by = 10

# Affiche tous les cours d'une année
class CoursListViewAnne (CoursListView):
	def get_queryset(self): 
		dateDebut = datetime(int(self.args[0]), 1, 1, 0, 0, 0)
		dateFin = datetime(int(self.args[0]), 12, 31, 23, 59, 59)

		return Cours.objects.filter(dateDebut__gte = dateDebut, dateFin__lte = dateFin)

# Affiche tous les cours d'un mois
class CoursListViewMois (CoursListView):
	def get_queryset(self):
		r = monthrange(int(self.args[0]), int(self.args[1])) # Pour connaître le nombre de jours dans le mois
		nbJours = r[1]

		dateDebut = datetime(int(self.args[0]), int(self.args[1]), 1, 0, 0, 0)
		dateFin = datetime(int(self.args[0]), int(self.args[1]), nbJours, 23, 59, 59)
		return Cours.objects.filter(dateDebut__gte = dateDebut, dateFin__lte = dateFin)

# Affiche tous les cours d'un jour
class CoursListViewJour (CoursListView):
	def get_queryset(self):
		dateDebut = datetime(int(self.args[0]), int(self.args[1]), int(self.args[2]), 0, 0, 0)
		dateFin = datetime(int(self.args[0]), int(self.args[1]), int(self.args[2]), 23, 59, 59)
		return Cours.objects.filter(dateDebut__gte = dateDebut, dateFin__lte = dateFin)

@login_required
def consultationCours(request, cours_id):
	cours = get_object_or_404(Cours, pk=cours_id)
	absences = Absence.objects.filter(cours_id = cours_id)

	return render(request, 'absences/consultationCours.html', {'cours':cours, 'absences':absences})

@permission_required('absences.add_absence')
def saisieAbsences(request, cours_id):
	cours = get_object_or_404(Cours, pk=cours_id)
	etudiants = []

	#Si la saisie a déjà été effectuée pour ce cours, on redirige vers l'index
	if not cours.saisieEffectuee:
		if request.method == 'POST':
			etudiants = request.POST.getlist('etudiants') #ids des étudiants sélectionnés
			for etudiant in etudiants:
				absence = Absence(etudiant_id=etudiant, cours_id=cours_id)
				absence.save()

				# vérifier s'il existe un justificatif qui prend en compte la date
				justificatifs = Justificatif.objects.filter(matiere = absence.cours.matiere.id, user = etudiant)
				
				# is la date du justif correspond à celle de l'absence, on justifie
				for justificatif in justificatifs:
					if ((absence.cours.dateDebut <= justificatif.dateDebut and absence.cours.dateFin <= justificatif.dateFin) or (absence.cours.dateDebut >= justificatif.dateDebut and absence.cours.dateFin >= justificatif.dateFin) or (absence.cours.dateDebut <= justificatif.dateDebut and absence.cours.dateFin >= justificatif.dateFin) or (absence.cours.dateDebut >= justificatif.dateDebut and absence.cours.dateFin <= justificatif.dateFin)):
						absence.justifie = True
						absence.justificatif = justificatif
						absence.save()

			cours.saisieEffectuee = True
			cours.save()

			messages.success(request, 'Les étudiants absents ont bien été enregistrés.')
			return redirect('absences:consultationCours', cours_id=cours_id)
	else:
		messages.error(request, 'La saisie pour ce cours a déjà été effectuée.')
		return redirect(reverse('absences:index'))

	return render(request, 'absences/saisie.html', {'cours':cours, 'etudiants':etudiants})

def ajouterJustificatif(request, absence_id):
	absence = get_object_or_404(Absence, pk=absence_id)
	cours = absence.cours 
	error = False

	if request.method == 'POST':
		form = JustificatifForm(request.POST)

		if form.is_valid():
			raison = form.cleaned_data['raison']
			justificatif = Justificatif(genre=raison, dateDebut=cours.dateDebut, dateFin=cours.dateFin, user = absence.etudiant)
			justificatif.save()
			absence.justifie = True
			absence.justificatif = justificatif
			absence.save()
			messages.success(request, 'Le justification a bien été ajouté.')
			return redirect('absences:consultationCours', cours_id=cours.id)
			
	else:
		form = JustificatifForm()

	return render(request, 'absences/ajouterJustificatif.html',{'absence':absence, 'form':form})

def ajouterMultipleJustificatif(request):
	"""Aouter un justificatif pour plusieurs cours"""
	form = None

	if request.method == "POST":
		form = JustificatifMultipleForm(request.POST)

		if form.is_valid():
			etudiantObject = Etudiant.objects.get(user=form.cleaned_data['etudiant'])
			matieres = request.POST.getlist('matieres')
			matieres = [int(m) for m in matieres]
			dateDebut = form.cleaned_data['dateDebut']
			dateFin = form.cleaned_data['dateFin']
			raison = form.cleaned_data['raison']

			justificatif = Justificatif(genre=raison, dateDebut = dateDebut, dateFin = dateFin, user = etudiantObject)
			justificatif.save()
			justificatif.matiere.add(*matieres)
			justificatif.save()

			absences = Absence.objects.filter(etudiant_id = etudiantObject.id, justifie = False)
			for absence in absences:
				if ((absence.cours.dateDebut <= dateDebut and absence.cours.dateFin <= dateFin) or (absence.cours.dateDebut >= dateDebut and absence.cours.dateFin >= dateFin) or (absence.cours.dateDebut <= dateDebut and absence.cours.dateFin >= dateFin) or (absence.cours.dateDebut >= dateDebut and absence.cours.dateFin <= dateFin)) and (absence.cours.matiere.id in matieres):

					absence.justifie = True
					absence.justificatif = justificatif
					absence.save()
				
			messages.success(request, 'Le justificatif a bien été ajouté pour {0}.'.format(etudiantObject))
			return redirect('absences:listeCours')

		else:
			form = JustificatifMultipleForm(request.POST)
	else:
		form = JustificatifMultipleForm()

	return render(request, 'absences/ajouterJustificatifMultiple.html', {'form': form})