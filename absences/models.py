from django.db import models

class Cours (models.Model):
	dateDebut = models.DateTimeField(auto_now = True, auto_now_add = False)
	dateFin = models.DateTimeField(auto_now = True, auto_now_add = False)
	saisieEffectuee = models.BooleanField(default = False)
	matiere = models.ForeignKey(Matiere)
	donne_a = models.ForeignKey(Groupe)
	donne_par = models.ManyToManyField(Enseignant, related_name = 'donne_par')

class Matiere (models.Model):
	intitule = models.CharField(max_length = 200)

class Departement (models.Model):
	nom = models.CharField(max_length = 200)
	directeur = models.ForeignKey(Enseignant, related_name= 'a_pour_directeur')

class Justificatif (models.Model):
	genre = models.CharField(max_length = 200)
	dateDebut = models.DateTimeField(auto_now = False, auto_now_add = False)
	dateFin = models.DateTimeField(auto_now = False, auto_now_add = False)
	matiere = models.ManyToManyField(Justificatif, related_name = 'vaut_pour_la_matiere')

class Utilisateur(models.Model):
	identifiant: models.CharField(max_length=200)
	prenom: models.CharField(max_length=200)
	mdp: models.CharField(max_length=200)
	nom: models.CharField(max_length=200)
	mail: models.CharField(max_length=200)

class Secretaire(Utilisateur):
	
class Etudiant(Utilisateur):
	promotion: models.ForeignKey(Promotion)
	
	
class Enseignant(Utilisateur):
	
class Promotion:
	nom: models.CharField(max_length=200)
	responsable: models.ForeignKey(Enseignant)

class Groupe(models.Model):
	nom: models.CharField(max_length=200)
	etudiants: models.ManyToManyField(Etudiant, related_name='membresGroupe+')
	
class Absence:
	etudiant: models.ForeignKey(Etudiant)
	cours: models.ForeignKey(Cours)
	justifie: models.BooleanField(default=False)