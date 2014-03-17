from django.shortcuts import render
from django.http import HttpResponse
from absences.models import Etudiant

def listeEleve(request):
    listeEleve = Etudiant.objects.all()
    context = {'listeEleve': listeEleve}
    return render(request, 'absences/listeEleve.html', context)
    #output = ', '.join([e.prenom + " " +e.nom for e in listeEleve])
    #return HttpResponse(output)
    
def infosEleve(request, idEleve):
    try:
        eleve = Etudiant.objects.get(id=idEleve)
    except Etudiant.DoesNotExist:
        raise Http404
    return render(request, 'absences/infosEleve.html', {'eleve': eleve})
