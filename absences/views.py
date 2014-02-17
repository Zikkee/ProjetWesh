from django.shortcuts import render
from absences.models import Cours 
from django.http import HttpResponse

def listeCours (request):
	return HttpResponse("Coucou tout le monde")