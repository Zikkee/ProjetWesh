from django.conf.urls import patterns, url

from absences import views

urlpatterns = patterns('',
	#url(r'^$', views.index, name='index'),
	url(r'^cours/liste$', views.listeCours, name='listeCours')
)