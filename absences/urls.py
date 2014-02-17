from django.conf.urls import patterns, url

from absences import listeEleve

urlpatterns = patterns('',
    url(r'^$', listeEleve.listeEleve, name='listeEleve')
)

