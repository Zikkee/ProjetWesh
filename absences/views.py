from django.shortcuts import render
from absences.models import Cours 
from django.http import HttpResponse

def listeCours (request):
	listeCours = Cours.objects.all()
	return render(request, 'absences/listeCours.html', {'listeCours':listeCours})

def consultationCours(request, cours_id):
	return HttpResponse("consultation du cours " + cours_id)