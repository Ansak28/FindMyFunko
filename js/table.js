

// $('#editModal').on('show.bs.modal', function(e) {  
//     var getIdFromRow = $(e.relatedTarget).data('id');

//     $("#editTitle").val(getIdFromRow);

//     });

$(function () { 
    // ON SELECTING ROW 
    $(".btnUpdate").click(function () { 
//FINDING ELEMENTS OF ROWS AND STORING THEM IN VARIABLES 
        var a = 
 $(this).parents("tr").find(".idF").text(); 
        var c = 
 $(this).parents("tr").find(".precioF").text(); 
        var d = 
 $(this).parents("tr").find(".stockF").text(); 
 var b = 
 $(this).parents("tr").find(".nombreF").text(); 

        // CREATING DATA TO SHOW ON MODEL 
        $("#editTitle").val(a);
        $("#editPrecio").val(c);
        $("#editName").val(b);
        $("#editStock").val(d);

    }); 
}); 

$("#addBtn").on("click", function() {

    setTimeout(function() {
        $('#addModal').modal('show');
        $('body').find('#addModal').focus();
    }, 1000);
});