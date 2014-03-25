from absences.models import Absence, Etudiant

import pdb

def nbAbsencesNonJustifiees (request):
	try:
		etudiant = Etudiant.objects.get(user=request.user.id)
		nb = Absence.objects.filter(etudiant_id = etudiant.id, justifie = False).count()
	except:
		nb = 0
	return {'nbAbsencesNonJustifiees':nb}

def determinerGroupe(request):
	estEtudiant = False
	estSecretaire = False
	estEnseignant = False

	try:
		groupes = request.user.groups.all()
		for groupe in groupes:
			if groupe.name == 'Etudiants':
				estEtudiant = True
			if groupe.name == 'Secretaires':
				estSecretaire = True
			if groupe.name == 'Enseignants':
				estEnseignant = True
	except:
		estEnseignant = False
		estEtudiant = False
		estSecretaire = False

	return {'estEtudiant':estEtudiant, 'estEnseignant':estEnseignant, 'estSecretaire':estSecretaire}