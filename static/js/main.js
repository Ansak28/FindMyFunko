document.getElementById("btnForm1").onclick = function() {

    var valorN =validarEmpty(document.getElementById("fNombre"));
    var valorA =validarEmpty(document.getElementById("fApellidos"));
    var valorNa =validarEmpty(document.getElementById("fNac"));
    var valorE =validarEmpty(document.getElementById("fEmail"));
    var valorT =validarEmpty(document.getElementById("fTelf"));
    var valorD =validarEmpty(document.getElementById("fDni"));

    if(valorN == false || valorA == false || valorNa == false || valorE == false || valorT == false || valorD == false){
        alert("Llene todos los campos"); 

    }else{
        $('.nivo a[href="#menu1"]').tab('show');
        document.getElementById("home").classList.add("disabled")

    }

};

document.getElementById("btnForm2").onclick = function() {

    var valorN =validarEmpty(document.getElementById("fTienda"));
    var valorA =validarEmpty(document.getElementById("fDireccion"));
    var valorNa =validarEmpty(document.getElementById("fEmailBuss"));
    var valorE =validarEmpty(document.getElementById("fTelfTie"));


    if(valorN == false || valorA == false || valorNa == false || valorE == false ){
        alert("Llene todos los campos"); 

    }else{
        $('.nivo a[href="#menu2"]').tab('show');

        document.getElementById("home").classList.add("disabled")

    }

};

function validarEmpty(parametro){

     if (parametro.value.length == 0)
      { 	
        parametro.style.borderBottomColor = "red"
         return false; 
      }  	
      return true; 
}

document.getElementById("fNombre").onchange = function(){ document.getElementById("fNombre").style.borderBottomColor = "#83A4C5"}
document.getElementById("fApellidos").onchange = function(){ document.getElementById("fApellidos").style.borderBottomColor = "#83A4C5"}
document.getElementById("fNac").onchange = function(){ document.getElementById("fNac").style.borderBottomColor = "#83A4C5"}
document.getElementById("fEmail").onchange = function(){ document.getElementById("fEmail").style.borderBottomColor = "#83A4C5"}
document.getElementById("fTelf").onchange = function(){ document.getElementById("fTelf").style.borderBottomColor = "#83A4C5"}
document.getElementById("fDni").onchange = function(){ document.getElementById("fDni").style.borderBottomColor = "#83A4C5"}
document.getElementById("fTienda").onchange = function(){ document.getElementById("fTienda").style.borderBottomColor = "#83A4C5"}
document.getElementById("fDireccion").onchange = function(){ document.getElementById("fDireccion").style.borderBottomColor = "#83A4C5"}
document.getElementById("fEmailBuss").onchange = function(){ document.getElementById("fEmailBuss").style.borderBottomColor = "#83A4C5"}
document.getElementById("fTelfTie").onchange = function(){ document.getElementById("fTelfTie").style.borderBottomColor = "#83A4C5"}


document.getElementById("btnVolverForm2").onclick = function() {
    $('.nivo a[href="#home"]').tab('show');
    document.getElementById("menu1").classList.add("disabled")
}

// $(function(){
//     $('#editModal').modal({
//         keyboard: true,
//         backdrop: "static",
//         show:false,
        
//     }).on('show', function(){
//           var getIdFromRow = $(this).data('orderid');
//         //make your ajax call populate items or what even you need
//         $(this).find('#editTitle').html($('<b> Order Id selected: ' + getIdFromRow  + '</b>'))
//     });
    
//     $(".table-striped").find('tr[data-target]').on('click', function(){
//         //or do your operations here instead of on show of modal to populate values to modal.
//          $('#editModal').data('orderid',$(this).data('id'));
//     });
    
// });
