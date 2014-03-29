from absences.models import Absence, Etudiant, Secretaire, Enseignant, Cours
from datetime import datetime

import pdb

def getNombres (request):
	nb = {}
	nb['absences'] = 0
	nb['nonSaisis'] = 0

	try:
		etudiant = Etudiant.objects.get(user=request.user)
		nb['absences'] = Absence.objects.filter(etudiant = etudiant, justifie = False).count()
	except:
		nb['absences'] = 0
		try:
			enseignant = Enseignant.objects.get(user=request.user)
			cours = Cours.objects.filter(donne_par = enseignant, saisieEffectuee = False, dateFin__lte = datetime.now())
			nb['nonSaisis'] = cours.count()
		except:
			nb['nonSaisis'] = 0

	return {'nb':nb}

def determinerGroupe(request):
	groupeUtilisateur = {}
	groupeUtilisateur['etudiant'] = None
	groupeUtilisateur['secretaire'] = None
	groupeUtilisateur['enseignant'] = None

	try:
		groupes = request.user.groups.all()
		for groupe in groupes:
			if groupe.name == 'Etudiants':
				groupeUtilisateur['etudiant'] = Etudiant.objects.get(user=request.user.id)
			elif groupe.name == 'Secretaires':
				groupeUtilisateur['secretaire'] = Secretaire.objects.get(user=request.user.id)
			elif groupe.name == 'Enseignants':
				groupeUtilisateur['enseignant'] = Enseignant.objects.get(user=request.user.id)
	except:
		groupeUtilisateur['etudiant'] = None
		groupeUtilisateur['secretaire'] = None
		groupeUtilisateur['enseignant'] = None

	# pdb.set_trace()
	return {'groupeUtilisateur':groupeUtilisateur}