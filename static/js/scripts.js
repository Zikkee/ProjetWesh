$('#valid-saisie').click(function() {
	var conf = confirm("Confirmez-vous votre saisie ?");
});

function remplirPopupJustificatif(idAbsence) {
    "use strict";
    var justificatif;
    $.ajax({
        url: '../../obtenirJustificatif/'+idAbsence,
        success: function(data) {
            justificatif = data;
        },
        failure: function() {
            justificatif = "Impossible de récupérer le justificatif !";
        },
        complete: function() {
            document.getElementById('justificatifPopup').getElementsByClassName('modal-body')[0].innerHTML = justificatif;
        }
}); 
}
