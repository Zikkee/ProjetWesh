from django.conf.urls import patterns, url

from absences import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^cours/liste/$', views.CoursListView.as_view(), name='listeCours'),
	url(r'^cours/liste/(\d{4})/$', views.CoursListViewAnne.as_view(), name='listeCoursAnnee'),
	url(r'^cours/liste/(\d{4})/(\d{2})/$', views.CoursListViewMois.as_view(), name='listeCoursMois'),
	url(r'^cours/liste/(\d{4})/(\d{2})/(\d{2})/$', views.CoursListViewJour.as_view(), name='listeCoursJour'),
	url(r'^cours/(?P<cours_id>\d+)/$', views.consultationCours, name='consultationCours'),
)