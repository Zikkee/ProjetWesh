#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout	
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count

from absences.models import Cours, Absence, Justificatif, Etudiant, Groupe, Enseignant, Matiere, Promotion
from absences.forms import ConnexionForm, JustificatifForm, JustificatifMultipleForm

from datetime import datetime
from calendar import monthrange


#DEBUG 


import pdb


# Vue de la page d'index
def index(request):
	return render(request, 'absences/index.html')

# Vue permettant la connexion d'un utilisateur
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
			error = True
	else:
		form = ConnexionForm()

	if error:
		messages.error(request, 'Vos identifiants ne sont pas corrects.')
	return render(request, 'absences/connexion.html', {'form':form})

#Vue permettant la déconnexion
@login_required
def deconnexion(request):
	logout(request)
	return redirect(reverse('absences:index'))

# Affiche tous les cours de la bdd
# @permission_required('absences.add_cours')
class CoursListView(ListView):
	model = Cours
	context_object_name = 'listeCours'
	template_name = 'absences/listeCours.html'
	paginate_by = 10

# Affiche tous les cours d'une année
# @permission_required('absences.add_cours')
class CoursListViewAnne (CoursListView):
	def get_queryset(self): 
		dateDebut = datetime(int(self.args[0]), 1, 1, 0, 0, 0)
		dateFin = datetime(int(self.args[0]), 12, 31, 23, 59, 59)

		return Cours.objects.filter(dateDebut__gte = dateDebut, dateFin__lte = dateFin)

# Affiche tous les cours d'un mois
# @permission_required('absences.add_cours')
class CoursListViewMois (CoursListView):
	def get_queryset(self):
		r = monthrange(int(self.args[0]), int(self.args[1])) # Pour connaître le nombre de jours dans le mois
		nbJours = r[1]

		dateDebut = datetime(int(self.args[0]), int(self.args[1]), 1, 0, 0, 0)
		dateFin = datetime(int(self.args[0]), int(self.args[1]), nbJours, 23, 59, 59)
		return Cours.objects.filter(dateDebut__gte = dateDebut, dateFin__lte = dateFin)

# Affiche tous les cours d'un jour
# @permission_required('absences.add_cours')
class CoursListViewJour (CoursListView):
	def get_queryset(self):
		dateDebut = datetime(int(self.args[0]), int(self.args[1]), int(self.args[2]), 0, 0, 0)
		dateFin = datetime(int(self.args[0]), int(self.args[1]), int(self.args[2]), 23, 59, 59)
		return Cours.objects.filter(dateDebut__gte = dateDebut, dateFin__lte = dateFin)

# Vue resensant tous les cours dispensés par un enseignant dont les absences n'ont pas été renseignées
@permission_required('absences.add_absence')
def mesCours(request):
	enseignant = Enseignant.objects.get(user=request.user.id)
	cours = Cours.objects.filter(dateFin__lte = datetime.now(), donne_par__id= enseignant.id, saisieEffectuee = False).order_by('-dateFin')

	return render(request, 'absences/listeCours.html', {'listeCours':cours, 'nonRenseignes':True})

# Vue permettant de voir les détails d'un cours donné
@login_required
def consultationCours(request, cours_id):
	cours = get_object_or_404(Cours, pk=cours_id)
	absences = Absence.objects.filter(cours_id = cours_id)

	return render(request, 'absences/consultationCours.html', {'cours':cours, 'absences':absences})

# Vue permettant de saisir les absences d'un cours donné 
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

	return render(request, 'absences/saisie.html', {'cours':cours})
	
# Vue permettant de voir la liste des élèves
@login_required
def listeEleve(request):
	listeEleve = Etudiant.objects.all()
	dicoInfos = {}
	for e in listeEleve:
		groupesEtudiant = Groupe.objects.filter(etudiants=e)
		dicoInfos[e] = groupesEtudiant
	context = {'infos': dicoInfos}
	return render(request, 'absences/listeEleve.html', context)

# Vue permettant de voir les détails d'un élève donné
@login_required
def infosEleve(request, idEleve = 0):
	if idEleve != 0:
		eleve = get_object_or_404(Etudiant, id=idEleve)
	else:
		eleve = get_object_or_404(Etudiant, user=request.user.id)

	absences = Absence.objects.filter(etudiant=eleve)
	return render(request, 'absences/infosEleve.html', {'eleve': eleve, 'absences':absences, 'own':True})

# Vue permettant, pour un étudiant connecté, de voir ses absences
@login_required
def mesAbsences(request):
	return infosEleve(request)

# Vue permettant de voir les détails d'une promotion
@login_required
def infosPromotion(request, idPromotion):
	promo = get_object_or_404(Promotion, id=idPromotion)
	eleves = Etudiant.objects.filter(promotion=promo)
	dicoInfos = {}
	for e in eleves:
		groupesEtudiant = Groupe.objects.filter(etudiants=e)
		dicoInfos[e] = groupesEtudiant
	return render(request, 'absences/infosPromotion.html', {'promotion': promo, 'infos': dicoInfos})

# Vue permettant d'ajouter un justificatif pour une absence donnée
@permission_required('absences.add_justificatif')
def ajouterJustificatif(request, absence_id, page_precedente, id_precedent):
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

# Vue permettant d'ajouter un justificatif pour plusieurs matières en même temps et pour une période donnée
@permission_required('absences.add_justificatif')
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

	return render(request, 'absences/ajouterJustificatifMultiple.html', {'form':form})

# Permet de visualiser un justificatif donnée
def obtenirJustificatif(request, idAbsence):
	absence = get_object_or_404(Absence, id=idAbsence)
	justificatif = absence.justificatif
	
	return HttpResponse(justificatif.genre)

# Pour un étudiant donné, permet de voir ses statistiques
def mesStatistiques(request, idEtudiant = 0):
	
	if idEtudiant == 0:
		etudiant = get_object_or_404(Etudiant, user=request.user.id)
	else:
		etudiant = get_object_or_404(Etudiant, pk=idEtudiant)

	nb = {}
	nb['nonJustifiees'] = {}
	nb['justifiees'] = {} 

	nb['nonJustifiees']['nb'] = Absence.objects.filter(etudiant = etudiant, justifie = False).count()
	nb['nonJustifiees']['name'] = 'Non justifiées'

	nb['justifiees']['nb'] = Absence.objects.filter(etudiant = etudiant, justifie = True).count()
	nb['justifiees']['name'] = 'Justifiées'

	nb['total'] = nb['justifiees']['nb'] + nb['nonJustifiees']['nb']

	absences = Absence.objects.filter(etudiant = etudiant)
	listeAbsences = {}

	for absence in absences:
		matiere = absence.cours.matiere.intitule
		if not matiere in listeAbsences.keys():
			listeAbsences[matiere] = 1
		else:
			listeAbsences[matiere] += 1

	return render(request, 'absences/statistiquesEtudiant.html', {'nb':nb, 'listeAbsences':listeAbsences})

# Permet de voir les statistiques d'un étudiant donné
def statistiquesEtudiant(request, idEtudiant):
	return mesStatistiques(request, idEtudiant)

#Permet de voir les statistiques générales sur les absences 
def statistiquesGenerales(request):

	# Absences justifiées - non justifiées
	absencesNonJustifiees = Absence.objects.filter(justifie = False).count()
	absencesJustifiees = Absence.objects.filter(justifie = True).count()
	totalAbsences = absencesJustifiees+absencesNonJustifiees

	# 5 matières avec le plus d'absents
	listeAbsencesMatieres = {}

	matieres = Matiere.objects.all()
	for matiere in matieres:
		listeAbsencesMatieres[matiere] = Absence.objects.filter(cours__matiere = matiere).count()

	sortedListeAbsencesMatieres = sorted(listeAbsencesMatieres.items(), key=lambda x: x[1], reverse=True)
	listeAbsencesMatieres = sortedListeAbsencesMatieres[:5]

	# 5 etudiants les plus absents
	etudiantsAbsents = Etudiant.objects.annotate(num_abs=Count('absence')).order_by('-num_abs')[:5]

	return render(request, 'absences/statistiquesGenerales.html', {'listeAbsencesMatieres': listeAbsencesMatieres, 'absencesNonJustifiees':absencesNonJustifiees, 'absencesJustifiees':absencesJustifiees, 'totalAbsences':totalAbsences, 'etudiantsAbsents':etudiantsAbsents})
