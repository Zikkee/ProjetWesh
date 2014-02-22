from django.conf.urls import patterns, url

from absences import views

urlpatterns = patterns('',
	#url(r'^$', views.absences.index, name='index'),
	url(r'^cours/liste/(\d{4})/(\d{2})/(\d{2})/$', views.CoursListView.as_view(), name='listeCours'),
	#url(r'^cours/liste/(\w+)/$', views.CoursListView.as_view(), name='listeCours'),
	url(r'^cours/(?P<cours_id>\d+)/$', views.consultationCours, name='consultationCours'),
)