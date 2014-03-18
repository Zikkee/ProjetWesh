from django.db import models
from django.contrib.auth.models import User



class Utilisateur(models.Model):
	user = models.OneToOneField(User)
	
	def __unicode__(self):
		return self.user.first_name + " " + self.user.last_name

class Secretaire(Utilisateur):
	pass
	
class Enseignant(Utilisateur):
	pass

class Promotion(models.Model):
	nom = models.CharField(max_length=200)
	responsable = models.ForeignKey(Enseignant)

	def __unicode__(self):
		return self.nom

class Matiere (models.Model):
	intitule = models.CharField(max_length = 200)
	
	def __unicode__(self):
		return self.intitule

class Etudiant(Utilisateur):
	promotion = models.ForeignKey(Promotion)
	
class Groupe(models.Model):
	nom = models.CharField(max_length=200)
	etudiants = models.ManyToManyField(Etudiant, related_name='membresGroupe+')

	def __unicode__(self):
		return self.nom	

class Cours (models.Model):
	dateDebut = models.DateTimeField(auto_now = True, auto_now_add = False)
	dateFin = models.DateTimeField(auto_now = True, auto_now_add = False)
	saisieEffectuee = models.BooleanField(default = False)
	matiere = models.ForeignKey(Matiere)
	donne_a = models.ManyToManyField(Groupe, related_name='donne_a')
	donne_par = models.ManyToManyField(Enseignant, related_name = 'donne_par')

	def __unicode__(self):
		return self.matiere.intitule

class Departement (models.Model):
	nom = models.CharField(max_length = 200)
	directeur = models.ForeignKey(Enseignant, related_name= 'a_pour_directeur')
	
	def __unicode__(self):
		return self.nom

class Justificatif (models.Model):
	genre = models.CharField(max_length = 200)
	dateDebut = models.DateTimeField(auto_now = False, auto_now_add = False)
	dateFin = models.DateTimeField(auto_now = False, auto_now_add = False)
	matiere = models.ManyToManyField(Matiere, related_name = 'vaut_pour_la_matiere')
	
	class Meta:
		permissions = (
			('can_ajouterJustificatif', 'Peut ajouter un justificatif'),
			('can_modifierJustificatif', 'Peut modifier un justificatif'),
		)

class Absence (models.Model):
	etudiant = models.ForeignKey(Etudiant)
	cours = models.ForeignKey(Cours)
	justifie = models.BooleanField(default=False)
	justificatif = models.ForeignKey(Justificatif, null=True,blank=True)