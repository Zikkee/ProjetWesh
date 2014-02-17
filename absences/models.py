from django.db import models

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
