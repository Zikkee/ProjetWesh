from django.conf.urls import patterns, url

from absences import views

urlpatterns = patterns('',
    url(r'^eleves/$', views.listeEleve, name='listeEleve'),
    url(r'^eleves/liste/(?P<idEleve>\d+)/$', views.infosEleve, name='infosEleve')
)
