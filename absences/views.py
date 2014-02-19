#-*- coding: utf-8 -*-

from django.shortcuts import render
from absences.models import Cours 
from django.http import HttpResponse
from django.views.generic.list import ListView

from datetime import datetime

class CoursListView(ListView):
	model = Cours
	context_object_name = 'listeCours' #permet de donner un nom autre que object_list pour la variable
	template_name = 'absences/listeCours.html' #redéfinition du template, au lieu de cours_list.html

	def get_queryset(self):
		if self.args[0]:
			dateAujourdhuiDebut = datetime.now()
			dateAujourdhuiFin = datetime.now()
			# dateAujourdhuiDebut = datetime(int(self.args[0]), int(self.args[1]), int(self.args[2]), 0, 0, 0)
			# dateAujourdhuiFin = datetime(int(self.args[0]), int(self.args[1]), int(self.args[2]), 23, 59, 59)
		else:
			dateAujourdhuiDebut = datetime.now().replace(hour=0, minute=0, second=0)
			dateAujourdhuiFin = datetime.now().replace(hour=23, minute=59, second=59)

		#permet de filtrer pour une date donnée (si pas de date, date d'aujourd'hui par défaut)
		return Cours.objects.filter(dateDebut__gte = dateAujourdhuiDebut, dateFin__lte = dateAujourdhuiFin)

def consultationCours(request, cours_id):
	return HttpResponse("consultation du cours " + cours_id)