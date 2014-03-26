from absences.models import Absence, Etudiant, Secretaire, Enseignant

import pdb

def nbAbsencesNonJustifiees (request):
	try:
		etudiant = Etudiant.objects.get(user=request.user.id)
		nb = Absence.objects.filter(etudiant_id = etudiant.id, justifie = False).count()
	except:
		nb = 0
	return {'nbAbsencesNonJustifiees':nb}

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

	return {'groupeUtilisateur':groupeUtilisateur}