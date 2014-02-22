#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

from absences.models import Cours 

from datetime import datetime
from calendar import monthrange

def index(request):
	return render(request, 'absences/index.html')

# Affiche tous les cours de la bdd
class CoursListView(ListView):
	model = Cours
	context_object_name = 'listeCours'
	template_name = 'absences/listeCours.html'
	paginate_by = 1

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

def consultationCours(request, cours_id):
	return HttpResponse("consultation du cours " + cours_id)