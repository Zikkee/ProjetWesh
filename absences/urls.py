from django.conf.urls import patterns, url

from absences import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^connexion/$', views.connexion, name='connexion'),
	url(r'^deconnexion/$', views.deconnexion, name='deconnexion'),
	url(r'^cours/liste/$', views.CoursListView.as_view(), name='listeCours'),
	url(r'^cours/liste/(\d{4})/$', views.CoursListViewAnne.as_view(), name='listeCoursAnnee'),
	url(r'^cours/liste/(\d{4})/(\d{2})/$', views.CoursListViewMois.as_view(), name='listeCoursMois'),
	url(r'^cours/liste/(\d{4})/(\d{2})/(\d{2})/$', views.CoursListViewJour.as_view(), name='listeCoursJour'),
	url(r'^cours/(?P<cours_id>\d+)/$', views.consultationCours, name='consultationCours'),
	url(r'^cours/(?P<cours_id>\d+)/saisie/$', views.saisieAbsences, name='saisieAbsences'),
	url(r'^justificatif/ajouter/(?P<absence_id>\d+)/$', views.ajouterJustificatif, name="ajouteJustificatif"),
	url(r'^eleves/$', views.listeEleve, name='listeEleve'),
	url(r'^eleves/liste/(?P<idEleve>\d+)/$', views.infosEleve, name='infosEleve'),
	url(r'^promotions/(?P<idPromotion>\d+)/$', views.infosPromotion, name='infosPromotion')
)