#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout	
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from absences.models import Cours, Absence
from absences.forms import ConnexionForm

from datetime import datetime
from calendar import monthrange

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
			cours.saisieEffectuee = True
			cours.save()

			messages.success(request, 'Les étudiants absents ont bien été enregistrés.')
			return redirect('absences:index')
	else:
		messages.error(request, 'La saisie pour ce cours a déjà été effectuée.')
		return redirect(reverse('absences:index'))

	return render(request, 'absences/saisie.html', {'cours':cours, 'etudiants':etudiants})